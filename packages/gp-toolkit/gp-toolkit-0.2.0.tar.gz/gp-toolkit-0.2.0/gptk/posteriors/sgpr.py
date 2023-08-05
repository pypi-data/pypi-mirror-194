import tensorflow as tf

from ..linalg import gramian, triangular_solvevec
from ..conditionals.utils import compute_projections, scale_mvn

from gpflow.config import default_float


def precursor(Kmm_linop: tf.linalg.LinearOperator, Kmn: tf.Tensor, noise_scale):

    # TODO(LT): Add support for rank >= 2 noise_scale.

    n_inducing = Kmm_linop.domain_dimension_tensor()

    Lm_linop = Kmm_linop.cholesky()  # [..., P, M, M]

    # TODO(LT): add tests for this
    # if rank is greater than or equal to 2, expand the -2nd dim
    # if tf.rank(noise_scale) > 1:
    #     noise_scale = tf.expand_dims(noise_scale, axis=-2)

    # Lm^{-1} Kmn / sigma; [..., P, M, M] [..., P, M, N] -> [..., P, M, N]
    Lm_inv_Kmn_scaled = Lm_linop.solve(Kmn / noise_scale)

    # sigma^2 Lm^{-1} Kmn Knm Lm^{-T} + I; [..., P, M, M]
    B = tf.linalg.matmul(Lm_inv_Kmn_scaled, Lm_inv_Kmn_scaled, adjoint_b=True)
    B += tf.eye(n_inducing, dtype=default_float())

    scale_inv_transpose = tf.linalg.cholesky(B)  # [..., P, M, M]

    return Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose


def _trace(Lm_inv_Kmn_scaled: tf.Tensor, Knn: tf.Tensor, noise_scale):

    # Knn / sigma^2; [..., P, N]
    Knn_scaled = Knn / tf.square(noise_scale)

    # [..., P, N, M]
    Knm_Lm_inv_transpose = tf.linalg.matrix_transpose(Lm_inv_Kmn_scaled)
    # Qmm / sigma^2; [..., P, M]
    Qmm_scaled = gramian(Knm_Lm_inv_transpose, diag=True)

    # [..., P, N] -> [..., P]
    trace = tf.reduce_sum(Knn_scaled, axis=-1)
    # [..., P, M] -> [..., P]
    trace -= tf.reduce_sum(Qmm_scaled, axis=-1)

    return trace


def _log_abs_det(Lm_inv_Kmn_scaled, scale_inv_transpose,
                 Knn: tf.Tensor, noise_scale):

    # [..., P, M, M] -> [..., P, M] -> [..., P]
    half_log_abs_det = tf.reduce_sum(tf.math.log(tf.linalg.diag_part(scale_inv_transpose)), axis=-1)

    # Broadcast to shape with trailing dimension N
    # scalars: [] -> [N]; arrays: [..., P, 1] or [..., P, N] -> [..., P, N]
    noise_scale *= tf.ones(shape=Knn.shape[-1:], dtype=default_float())

    # Sum over trailing dimension; [..., P, N] -> [..., P]
    half_log_var = tf.reduce_sum(tf.math.log(noise_scale), axis=-1)

    trace = _trace(Lm_inv_Kmn_scaled, Knn, noise_scale)

    return - (half_log_abs_det + half_log_var + .5 * trace)


def _quadratic(Lm_inv_Kmn_scaled, scale_inv_transpose, 
               err: tf.Tensor, noise_scale):
    """
    The terms of the ELBO that are quadratic in the target vector.
    """
    c = function(Lm_inv_Kmn_scaled, scale_inv_transpose, err, noise_scale)

    err_inner_prod = tf.reduce_sum(tf.square(err / noise_scale), axis=-1)  # / tf.square(noise_scale)  # [..., P, N] -> [..., P]
    c_inner_prod = tf.reduce_sum(tf.square(c), axis=-1)  # [..., P, M] -> [..., P]

    return -.5 * (err_inner_prod - c_inner_prod)


def function(Lm_inv_Kmn_scaled, scale_inv_transpose, err: tf.Tensor, noise_scale):
    # sqrt(beta) Lm^{-1} Kmn y; [..., P, M, N]  [..., P, N] -> [..., P, M]
    Aerr = tf.linalg.matvec(Lm_inv_Kmn_scaled, err / noise_scale)
    return triangular_solvevec(scale_inv_transpose, Aerr)  # [..., P, M]


def optimal_posterior(Kmm_linop: tf.linalg.LinearOperator, 
                      Kmn, err: tf.Tensor, noise_scale, diag_cov: bool):

    Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)
    Lm_inv_Kmm = Lm_linop.solve(Kmm_linop).to_dense()  # [..., P, M, M]

    c = function(Lm_inv_Kmn_scaled, scale_inv_transpose, err, noise_scale)
    # LB^{-1} Lm^{-1} Kmm; [..., P, M, M] [..., P, M, M] -> [..., P, M, M]
    scale = tf.linalg.triangular_solve(scale_inv_transpose, Lm_inv_Kmm)

    # Kmm Lm^{-T} B^{-1} Lm^{-1} Kmn y; [..., P, M, M] [..., P, M] -> [..., P, M]
    loc = tf.linalg.matvec(scale, c, adjoint_a=True)
    cov = gramian(scale, diag=diag_cov)  # [..., P, M] or [..., P, M, M]

    return loc, cov


def predictive(Kmm_linop, Ktt: tf.Tensor, Kmt: tf.Tensor, Kmn: tf.Tensor,
               err: tf.Tensor, noise_scale, diag_cov: bool):

    Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)

    # Lm^{-1} Kmt; [..., P, M, M] [..., P, M, T] -> [..., P, M, T]
    Lm_inv_Kmt = Lm_linop.solve(Kmt)

    c = function(Lm_inv_Kmn_scaled, scale_inv_transpose, err, noise_scale)
    scale = tf.linalg.triangular_solve(scale_inv_transpose, Lm_inv_Kmt, lower=True)

    Qtt = gramian(Lm_inv_Kmt, diag=diag_cov)  # [..., P, T] or [..., P, T, T]

    loc = tf.linalg.matvec(scale, c, adjoint_a=True)
    cov = gramian(scale, diag=diag_cov)  # [..., P, T] or [..., P, T, T]
    cov += Ktt - Qtt  # [..., P, T] or [..., P, T, T]

    return loc, cov


def _predictive_alt(Kmm_linop, Ktt: tf.Tensor, Kmt: tf.Tensor, Kmn: tf.Tensor,
                    err: tf.Tensor, noise_scale, diag_cov: bool):

    Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)

    # sqrt(beta) Lm^{-1} Kmn y; [..., P, M, N]  [..., P, N] -> [..., P, M]
    Aerr = tf.linalg.matvec(Lm_inv_Kmn_scaled, err / noise_scale)

    # Lm^{-1} Kmt; [..., P, M, M] [..., P, M, T] -> [..., P, M, T]
    Lm_inv_Kmt = Lm_linop.solve(Kmt)

    qu_scale_linop = tf.linalg.LinearOperatorLowerTriangular(scale_inv_transpose)  # LB
    qu_scale_linop = tf.linalg.LinearOperatorAdjoint(qu_scale_linop)  # LB^T
    qu_scale_linop = tf.linalg.LinearOperatorInversion(qu_scale_linop)  # LB^{-T}

    # sqrt(beta) LB^{-1} Lm^{-1} Kmn y; [..., P, M, M] [..., P, M] -> [..., P, M]
    c = qu_scale_linop.matvec(Aerr, adjoint=True)

    # LB^{-T} c;  [..., P, M, M] [..., P, M] -> [..., P, M]
    qu_loc = qu_scale_linop.matvec(c) 
    # [..., N, N], [..., M, N]
    Qtt, Qmt = compute_projections(Lm_linop, Lm_inv_Kmt, white=True, diag_cov=diag_cov)

    # [..., P, N], [..., P, N] or [..., P, N, N]
    loc, cov = scale_mvn(Qmt, qu_loc, qu_scale_linop, diag_cov=diag_cov)
    cov += Ktt - Qtt

    return loc, cov

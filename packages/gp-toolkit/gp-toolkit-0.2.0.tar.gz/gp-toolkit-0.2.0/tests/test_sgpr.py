#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from gpflow.models.sgpr import SGPR_deprecated as SGPR2
from gpflow.config import default_float

from gptk.posteriors.sgpr import predictive, optimal_posterior, _quadratic, _log_abs_det, _trace, _predictive_alt, precursor
from gptk.conditionals.utils import to_positive_definite_linop

tfd = tfp.distributions


def test_precursor(Kmm, Kmn, train_data, kernel, inducing_variable, noise_variance, random_state):

    X_train, Y_train = train_data

    model2 = SGPR2(data=train_data,
                   kernel=kernel,
                   inducing_variable=inducing_variable,
                   noise_variance=noise_variance)

    common = model2._common_calculation()

    noise_scale = tf.sqrt(tf.constant(noise_variance, shape=(1,), dtype=default_float()))

    # Kmn = Kuf(inducing_variable, kernel, X_train)  # [..., P, M, N]
    # Kmm = Kuu(inducing_variable, kernel, jitter=default_jitter())  # [..., P, M, M]
    Kmm_linop = to_positive_definite_linop(Kmm)  # [..., P, M, M]

    Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)

    common = model2._common_calculation()

    np.testing.assert_allclose(common.L, Lm_linop.to_dense())

    # TODO(LT): Add meaningful (numerically stable) tests for these.
    # np.testing.assert_allclose(common.A, Lm_inv_Kmn_scaled, rtol=1e-5)
    # np.testing.assert_allclose(common.LB, scale_inv_transpose, rtol=1e-5)


def test_optimal_posterior(Kmm, Kmn, train_data, kernel, inducing_variable, noise_variance, random_state):

    Kmm_linop = to_positive_definite_linop(Kmm)  # [M, M]

    X_train, Y_train = train_data
    n_train, input_dim = X_train.shape

    model2 = SGPR2(data=train_data,
                   kernel=kernel,
                   inducing_variable=inducing_variable,
                   noise_variance=noise_variance)

    qu_loc2, qu_cov2 = model2.compute_qu()

    noise_scale = tf.sqrt(model2.likelihood.variance)
    noise_precision = tf.constant(1./model2.likelihood.variance,
                                  shape=(n_train,), 
                                  dtype=default_float())

    err = Y_train

    M = tf.linalg.LinearOperatorLowRankUpdate(
        Kmm_linop, Kmn, diag_update=noise_precision, is_diag_update_positive=True
    )  # not practical; less efficient when N > M

    L = M.cholesky()
    L_inv_Kmn = L.solve(Kmn)  # Tensor
    L_inv_Kmm = L.solve(Kmm_linop)  # LinearOperator

    qu_loc1 = L_inv_Kmm.matmul(L_inv_Kmn, adjoint=True) @ err / noise_variance

    qu_cov_linop = L_inv_Kmm.matmul(L_inv_Kmm, adjoint=True)
    qu_cov1 = qu_cov_linop.to_dense()

    # qu_var = qu_cov_linop.diag_part()
    # qu_scale = tf.sqrt(qu_var)

    np.testing.assert_allclose(qu_loc1, qu_loc2)
    np.testing.assert_allclose(qu_cov1, qu_cov2, rtol=1e-4)

    qu_loc3, qu_cov3 = optimal_posterior(Kmm_linop, Kmn, 
                                         err=tf.linalg.matrix_transpose(Y_train), 
                                         noise_scale=noise_scale, 
                                         diag_cov=False)

    qu_loc3 = tf.transpose(qu_loc3)
    qu_cov3 = tf.transpose(qu_cov3)

    np.testing.assert_allclose(qu_loc1, qu_loc3)
    np.testing.assert_allclose(qu_cov1, qu_cov3, rtol=1e-4)

    _, qu_var3 = optimal_posterior(Kmm_linop, Kmn, 
                                   err=tf.linalg.matrix_transpose(Y_train), 
                                   noise_scale=noise_scale, 
                                   diag_cov=True)

    np.testing.assert_allclose(qu_var3, tf.linalg.diag_part(qu_cov3))


def test_predictive(Kmm, Kmn, Kmt, Ktt, output_dim, train_data, X_test, kernel, inducing_variable, noise_variance, diag_cov, random_state):

    X_train, Y_train = train_data

    noise_scale = tf.sqrt(tf.constant(noise_variance, shape=(1,), dtype=default_float()))

    model2 = SGPR2(data=(X_train, Y_train), 
                   kernel=kernel,
                   inducing_variable=inducing_variable,
                   noise_variance=noise_variance)

    qf_loc2, qf_cov2 = model2.predict_f(X_test, full_cov=not diag_cov)

    Kmm_linop = to_positive_definite_linop(Kmm)  # [M, M]
    Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)

    err = tf.linalg.matrix_transpose(Y_train)  # [P, N]

    qf_loc1_T, qf_cov1_T = predictive(Kmm_linop, Ktt, Kmt, Kmn, err, noise_scale, diag_cov)

    if diag_cov:
        qf_cov1_T += tf.zeros((output_dim, 1), dtype=default_float())
    else:
        qf_cov1_T += tf.zeros((output_dim, 1, 1), dtype=default_float())

    qf_loc1 = tf.linalg.matrix_transpose(qf_loc1_T)
    qf_cov1 = tf.linalg.matrix_transpose(qf_cov1_T) if diag_cov else qf_cov1_T

    np.testing.assert_allclose(qf_loc1, qf_loc2)
    np.testing.assert_allclose(qf_cov1, qf_cov2)

    qf_loc3_T, qf_cov3_T = _predictive_alt(Kmm_linop, Ktt, Kmt, Kmn, err, noise_scale, diag_cov)

    if diag_cov:
        qf_cov3_T += tf.zeros((output_dim, 1), dtype=default_float())
    else:
        qf_cov3_T += tf.zeros((output_dim, 1, 1), dtype=default_float())

    qf_loc3 = tf.linalg.matrix_transpose(qf_loc3_T)
    qf_cov3 = tf.linalg.matrix_transpose(qf_cov3_T) if diag_cov else qf_cov3_T

    np.testing.assert_allclose(qf_loc2, qf_loc3)
    np.testing.assert_allclose(qf_cov2, qf_cov3)


def test_elbo(Kmm, Kmn, train_data, n_train, kernel, inducing_variable, noise_variance, random_state):

    X_train, Y_train = train_data

    noise_scale = tf.sqrt(tf.constant(noise_variance, shape=(1,), dtype=default_float()))

    model2 = SGPR2(data=train_data, 
                   kernel=kernel,
                   inducing_variable=inducing_variable,
                   noise_variance=noise_variance)
    elbo2 = model2.elbo()

    noise_variance = model2.likelihood.variance

    Knn = kernel(X_train, full_cov=False)
    # Kmm = Kuu(inducing_variable, kernel, jitter=default_jitter())  # [..., P, M, M]
    # Kmn = Kuf(inducing_variable, kernel, X_train)  # [..., P, M, N]
    Kmm_linop = to_positive_definite_linop(Kmm)  # [..., P, M, M]

    Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)
    Lm_inv_Kmn = Lm_linop.solve(Kmn)  # Tensor; [..., P, M, N]

    trace = _trace(Lm_inv_Kmn_scaled, Knn, noise_scale)

    cov_diag_factor = noise_variance * tf.ones(n_train, dtype=default_float())
    cov_perturb_factor = tf.linalg.matrix_transpose(Lm_inv_Kmn)  # [..., N, M]

    p = tfd.MultivariateNormalDiagPlusLowRankCovariance(
        cov_diag_factor=cov_diag_factor,
        cov_perturb_factor=cov_perturb_factor
    )

    err = tf.linalg.matrix_transpose(Y_train)  # [..., P, N]

    elbo_batch1 = p.log_prob(err) - .5 * trace  # [..., P]
    elbo1 = tf.reduce_sum(elbo_batch1, axis=-1)

    np.testing.assert_allclose(elbo1, elbo2)

    common = model2._common_calculation()
    quadratic2 = model2.quad_term(common)
    log_abs_det2 = model2.logdet_term(common)

    quadratic_batch1 = _quadratic(Lm_inv_Kmn_scaled, scale_inv_transpose, err, noise_scale)  # [P]

    log_abs_det1 = _log_abs_det(Lm_inv_Kmn_scaled, scale_inv_transpose, Knn, noise_scale)  # []
    log_abs_det_broad1 = log_abs_det1 + tf.zeros_like(quadratic_batch1, dtype=default_float())  # [P]

    np.testing.assert_allclose(tf.reduce_sum(quadratic_batch1, axis=0), quadratic2)
    np.testing.assert_allclose(tf.reduce_sum(log_abs_det_broad1, axis=0), log_abs_det2)

    const_batch = -.5 * np.log(2. * np.pi)  # []
    const_batch += tf.zeros(n_train, dtype=default_float())  # [N]
    const = tf.reduce_sum(const_batch, axis=-1)  # []

    elbo3 = tf.reduce_sum(quadratic_batch1 + log_abs_det1 + const, axis=0)

    np.testing.assert_allclose(elbo2, elbo3)

import numpy as np
import tensorflow as tf

from typing import Tuple

from gpflow.models.sgpr import SGPRBase_deprecated
from gpflow.covariances import Kuu, Kuf
from gpflow.base import InputData, MeanAndVariance
from gpflow.config import default_jitter, default_float

from ...posteriors.sgpr import (
    predictive,
    optimal_posterior,
    _quadratic,
    _log_abs_det,
    precursor
)


class SGPR(SGPRBase_deprecated):

    # TODO(ltiao): rename `num_latent_gps` to `output_dim` to be consistent 
    # with SVGP.

    def maximum_log_likelihood_objective(self) -> tf.Tensor:
        return self.elbo()

    def upper_bound(self):
        raise NotImplementedError("Not yet supported in `gp-toolkit`!")

    def elbo(self, loss_weights=None) -> tf.Tensor:
        if loss_weights is not None:
            raise NotImplementedError("Coming soon!")

        # TODO(ltiao): separate into helper method
        X_data, Y_data = self.data
        n_train = X_data.shape[0]

        err = Y_data - self.mean_function(X_data)
        target = tf.linalg.matrix_transpose(err)

        Kmm_linop = Kuu(self.inducing_variable, self.kernel, jitter=default_jitter())
        Kmn = Kuf(self.inducing_variable, self.kernel, X_data)
        Knn = self.kernel(X_data, full_cov=False)

        noise_scale = tf.sqrt(self.likelihood.variance)

        Lm_linop, Lm_inv_Kmn_scaled, scale_inv_transpose = precursor(Kmm_linop, Kmn, noise_scale)

        quadratic_batch = _quadratic(Lm_inv_Kmn_scaled, scale_inv_transpose, target, noise_scale)  # [P]
        log_abs_det = _log_abs_det(Lm_inv_Kmn_scaled, scale_inv_transpose, Knn, noise_scale)  # []
        const = -.5 * n_train * np.log(2. * np.pi)  # []

        return tf.reduce_sum(quadratic_batch + log_abs_det + const, axis=None)

    def predict_f(self, Xnew: InputData, full_cov: bool = False,
                  full_output_cov: bool = False) -> MeanAndVariance:

        diag_cov = not full_cov

        # TODO(ltiao): separate into helper method
        X_data, Y_data = self.data

        err = Y_data - self.mean_function(X_data)
        target = tf.linalg.matrix_transpose(err)

        Kmm_linop = Kuu(self.inducing_variable, self.kernel, jitter=default_jitter())
        Kmn = Kuf(self.inducing_variable, self.kernel, X_data)
        Kmt = Kuf(self.inducing_variable, self.kernel, Xnew)
        Ktt = self.kernel(Xnew, full_cov=full_cov)

        noise_scale = tf.sqrt(self.likelihood.variance)

        mean_transposed, cov_transposed = predictive(Kmm_linop, Ktt, Kmt, Kmn, 
                                                     target, noise_scale, diag_cov)
        mean = tf.linalg.matrix_transpose(mean_transposed)  # [..., P, T] -> [..., T, P]

        # TODO(ltiao): separate into helper method
        output_shape = mean_transposed.shape[:-1]  # [..., P]

        # [..., P, 1] if diag_cov else [..., P, 1, 1] 
        shape = (*output_shape, 1) if diag_cov else (*output_shape, 1, 1)

        # [T] -> [..., P, T] if diag_cov else [T, T] -> [..., P, T, T]
        cov_transposed += tf.zeros(shape, dtype=default_float())

        # [..., P, T] -> [..., T, P] if diag_cov else [..., P, T, T]
        cov = tf.linalg.matrix_transpose(cov_transposed) if diag_cov else cov_transposed

        return mean + self.mean_function(Xnew), cov

    def compute_qu(self, diag_cov=False) -> Tuple[tf.Tensor, tf.Tensor]:
        X_data, Y_data = self.data

        # TODO(ltiao): separate into helper method
        err = Y_data - self.mean_function(X_data)
        target = tf.linalg.matrix_transpose(err)

        noise_scale = tf.sqrt(self.likelihood.variance)

        Kmm_linop = Kuu(self.inducing_variable, self.kernel, jitter=default_jitter())
        Kmn = Kuf(self.inducing_variable, self.kernel, X_data)

        loc_transposed, cov_transposed = optimal_posterior(Kmm_linop, Kmn, 
                                                           target, noise_scale, 
                                                           diag_cov=diag_cov)

        # TODO(ltiao): separate into helper method
        output_shape = loc_transposed.shape[:-1]  # [..., P]

        # [..., P, 1] if diag_cov else [..., P, 1, 1] 
        shape = (*output_shape, 1) if diag_cov else (*output_shape, 1, 1)

        # [T] -> [..., P, T] if diag_cov else [T, T] -> [..., P, T, T]
        cov_transposed += tf.zeros(shape, dtype=default_float())

        loc = tf.linalg.matrix_transpose(loc_transposed)
        cov = tf.linalg.matrix_transpose(cov_transposed) if diag_cov else cov_transposed

        return loc, cov

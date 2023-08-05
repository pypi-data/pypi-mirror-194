#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest

import tensorflow as tf
import numpy as np

from gptk.gpflow.models.svgp import SVGP as SVGP1
from gptk.gpflow.models.sgpr import SGPR as SGPR1

from gptk.inducing_variables.base import InducingPointsExtended

from gptk.covariances import base
from gptk.conditionals import base
from gptk.divergences import base

from gpflow.models.svgp import SVGP_deprecated as SVGP2
from gpflow.models.sgpr import SGPR_deprecated as SGPR2


def test_sgpr(train_data, X_test, kernel, inducing_variable, noise_variance, diag_cov):

    full_cov = not diag_cov
    inducing_variable_plus = InducingPointsExtended.from_inducing_points(inducing_variable)

    model1 = SGPR1(data=train_data,
                   kernel=kernel,
                   inducing_variable=inducing_variable_plus,
                   noise_variance=noise_variance)

    model2 = SGPR2(data=train_data,
                   kernel=kernel,
                   inducing_variable=inducing_variable,
                   noise_variance=noise_variance)

    qf_loc_1, qf_cov_1 = model1.predict_f(X_test, full_cov=full_cov, full_output_cov=False)
    qf_loc_2, qf_cov_2 = model2.predict_f(X_test, full_cov=full_cov, full_output_cov=False)

    np.testing.assert_allclose(qf_loc_1, qf_loc_2)
    np.testing.assert_allclose(qf_cov_1, qf_cov_2)

    qu_loc_1, qu_cov_1 = model1.compute_qu()
    qu_loc_2, qu_cov_2 = model2.compute_qu()

    np.testing.assert_allclose(qu_loc_1, qu_loc_2)
    np.testing.assert_allclose(qu_cov_1, qu_cov_2)

    elbo1 = model1.elbo()
    elbo2 = model2.elbo()

    np.testing.assert_allclose(elbo1, elbo2)


@pytest.mark.parametrize("q_white", [False, True])
def test_svgp(X_test, likelihood, kernel, inducing_variable, q_white, q_diag, output_dim, diag_cov):

    full_cov = not diag_cov

    inducing_variable_plus = InducingPointsExtended.from_inducing_points(inducing_variable)

    model_1 = SVGP1.from_default(kernel, likelihood, inducing_variable_plus,
                                 q_white=q_white, q_diag=q_diag, output_dim=output_dim)

    q_mu = tf.transpose(model_1.q_loc)  # [M, P]
    q_sqrt = tf.transpose(model_1.q_scale_linop.diag_part()) if q_diag \
        else model_1.q_scale_linop.to_dense()

    model_2 = SVGP2(kernel, likelihood, inducing_variable,
                    num_latent_gps=output_dim, q_diag=q_diag, 
                    q_mu=q_mu, q_sqrt=q_sqrt, whiten=q_white)

    qf_loc_1, qf_cov_1 = model_1.predict_f(X_test, full_cov=full_cov, full_output_cov=False)
    qf_loc_2, qf_cov_2 = model_2.predict_f(X_test, full_cov=full_cov, full_output_cov=False)

    np.testing.assert_allclose(qf_loc_1, qf_loc_2)
    np.testing.assert_allclose(qf_cov_1, qf_cov_2)

    # np.testing.assert_allclose(model_1.prior_kl(), model_2.prior_kl())

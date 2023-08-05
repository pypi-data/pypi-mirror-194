#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest

import numpy as np
import tensorflow as tf

from gpflow.conditionals.util import base_conditional
from gptk.conditionals.base import _base_conditional_linop_compat, _base_conditional_linop
from gptk.conditionals.utils import to_positive_definite_linop, compute_projections, scale_mvn
from gptk.linalg import gramian


@pytest.mark.parametrize("white", [False, True])
def test_conditional(Kmm, Kmt, Ktt, kernel, q_loc, q_scale_linop, white, diag_cov):

    Kmm_linop = to_positive_definite_linop(Kmm)

    q_mu = tf.transpose(q_loc)  # [M, P]
    if isinstance(q_scale_linop, tf.linalg.LinearOperatorDiag):
        q_sqrt = tf.transpose(q_scale_linop.diag_part())  # [M, P]
    else:
        q_sqrt = q_scale_linop.to_dense()  # [P, M, M]

    mean1, cov1 = _base_conditional_linop_compat(Kmm_linop, Kmt, Ktt, q_loc, q_scale_linop, white, diag_cov=diag_cov)
    mean2, cov2 = base_conditional(Kmt, Kmm, Ktt, q_mu, q_sqrt=q_sqrt, white=white, full_cov=not diag_cov)

    np.testing.assert_allclose(mean1, mean2)
    np.testing.assert_allclose(cov1, cov2)


@pytest.mark.parametrize("output_shape", [(), (5,), (2, 3)])
def test_base_conditional_linop_broadcasting(output_shape, output_dim, n_test, n_inducing, q_loc, q_scale_linop, diag_cov, random_state):

    b = random_state.randn(output_dim, n_test, n_test)
    Knn = gramian(b, diag=diag_cov)

    # separate
    Kmt = random_state.randn(*output_shape, output_dim, n_inducing, n_test)
    a = random_state.randn(*output_shape, output_dim, n_inducing, n_inducing)
    Kmm_linop = to_positive_definite_linop(gramian(a, diag=False))

    mean, cov = _base_conditional_linop(Kmm_linop, Kmt, Knn, q_loc, q_scale_linop, white=False, diag_cov=diag_cov)

    assert mean.shape[:len(output_shape)+1] == cov.shape[:len(output_shape)+1] == (*output_shape, output_dim)

    # shared
    Kmt = random_state.randn(*output_shape, 1, n_inducing, n_test)
    a = random_state.randn(*output_shape, 1, n_inducing, n_inducing)
    Kmm_linop = to_positive_definite_linop(gramian(a, diag=False))

    mean, cov = _base_conditional_linop(Kmm_linop, Kmt, Knn, q_loc, q_scale_linop, white=False, diag_cov=diag_cov)

    assert mean.shape[:len(output_shape)+1] == cov.shape[:len(output_shape)+1] == (*output_shape, output_dim)

#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest

import numpy as np
import tensorflow as tf

from gpflow.kullback_leiblers import gauss_kl
from gptk.divergences.base import _base_kl_divergence_linop
from gptk.conditionals.utils import to_positive_definite_linop


@pytest.mark.parametrize("white", [False, True])
def test(Kmm, q_loc, q_scale_linop, white):

    if white:
        L = Lm_linop = None
    else:
        Kmm_linop = to_positive_definite_linop(Kmm)
        Lm_linop = Kmm_linop.cholesky()
        L = Lm_linop.to_dense()

    q_mu = tf.transpose(q_loc)  # [M, P]
    if isinstance(q_scale_linop, tf.linalg.LinearOperatorDiag):
        q_sqrt = tf.transpose(q_scale_linop.diag_part())  # [M, P]
    else:
        q_sqrt = q_scale_linop.to_dense()  # [P, M, M]

    kl_1 = _base_kl_divergence_linop(q_loc, q_scale_linop, Lm_linop)
    kl_2 = gauss_kl(q_mu, q_sqrt, K_cholesky=L)

    np.testing.assert_approx_equal(kl_1, kl_2)

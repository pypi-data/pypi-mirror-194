#!/usr/bin/env python

import tensorflow as tf
import tensorflow_probability as tfp

from gptk.datasets import load_snelson_1d, load_motorcycle, load_jura, make_circle, make_regression

kernels = tfp.math.psd_kernels


def test_load_snelson_1d():

    dataset = load_snelson_1d()

    assert dataset.data.shape == (200, 1)
    assert dataset.target.shape == (200, 1)


def test_load_motorcycle():

    dataset = load_motorcycle()

    assert dataset.data.shape == (94, 1)
    assert dataset.target.shape == (94, 1)


def test_load_jura():

    dataset = load_jura()

    assert dataset.data.shape == (259, 2)
    assert dataset.target.shape == (259, 7)


def test_make_circles(noise_variance, random_state):

    n_samples = 256
    X_train, Y_train = make_circle(n_samples, noise_scale=tf.sqrt(noise_variance), random_state=random_state)

    assert X_train.shape == (n_samples, 1)
    assert Y_train.shape == (n_samples, 2)


def test_make_regression(kernel, input_dim, output_dim, noise_variance, random_state):

    n_samples = 256

    # GPflow-style kernels
    covariance_fn = kernel.K

    X_train, Y_train = make_regression(covariance_fn, n_samples, input_dim, 
                                       output_dim, hidden_dim=None, 
                                       noise_variance=noise_variance,
                                       random_state=random_state)

    assert X_train.shape == (n_samples, input_dim)
    assert Y_train.shape == (n_samples, output_dim)


def test_make_regression_tfp(input_dim, output_dim, noise_variance, random_state):

    n_samples = 256

    # TensorFlow-Probability-style kernels
    kernel = kernels.MaternFiveHalves()

    def covariance_fn(X): 
        return kernel.matrix(X, X)

    X_train, Y_train = make_regression(covariance_fn, n_samples, input_dim, 
                                       output_dim, hidden_dim=None, 
                                       noise_variance=noise_variance,
                                       random_state=random_state)

    assert X_train.shape == (n_samples, input_dim)
    assert Y_train.shape == (n_samples, output_dim)

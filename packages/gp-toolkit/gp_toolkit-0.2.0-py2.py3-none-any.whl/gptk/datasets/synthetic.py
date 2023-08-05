import tensorflow as tf
import numpy as np

from sklearn.utils import check_random_state


def make_regression(covariance_fn, n_samples, input_dim, output_dim, 
                    hidden_dim=None, noise_variance=0.1,
                    xlim=(-1., 1.), sort=True, return_numpy=True,
                    random_state=None):

    rng = check_random_state(random_state)

    X = rng.uniform(*xlim, size=(n_samples, input_dim))  # [N, D]
    X.sort(axis=0) if sort else None

    K = covariance_fn(X)  # [..., P, N, N]

    tf.debugging.assert_rank_at_least(K, 2, "kernel matrix")

    K_noise = tf.linalg.set_diag(K, tf.linalg.diag_part(K) + noise_variance)
    L = tf.linalg.cholesky(K_noise)  # [..., P, N, N]

    if hidden_dim is None:
        eps = rng.randn(output_dim, n_samples)  # [..., P, N]
        Y = tf.linalg.matvec(L, eps)  # [..., P, N, N] [..., P, N] -> [..., P, N] 
    else:
        eps = rng.randn(hidden_dim, n_samples)  # [..., P, N]
        Z = tf.linalg.matvec(L, eps)  # [..., P, N, N] [..., P, N] -> [..., P, N] 
        W = rng.randn(output_dim, Z.shape[-2])  # [Q, P]
        Y = tf.matmul(W, Z)  # [Q, P] [..., P, N] -> [..., Q, N]

    # TODO(LT): add option for this transpose operation
    Y = tf.linalg.matrix_transpose(Y)  # [..., N, Q] or # [..., N, P]

    if return_numpy:
        Y = Y.numpy()

    return X, Y


def make_circle(n_samples, noise_scale=0.1, sort=True, random_state=None):
    """
    Swiss Jura mineral concentration dataset.

    Examples
    --------

    .. plot::
        :include-source:
        :context: close-figs

        from gptk.datasets import make_circle

        n_samples = 128

        X, Y = make_circle(n_samples, random_state=8888)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.scatter(Y[..., 0], Y[..., 1], X.squeeze(axis=-1), c=np.arange(n_samples))

        ax.set_xlabel(r'$y_1$')
        ax.set_ylabel(r'$y_2$')
        ax.set_zlabel(r'$x$')

        plt.show()
    """

    rng = check_random_state(random_state)

    theta = rng.uniform(0., 2.*np.pi, n_samples)
    theta.sort(axis=0) if sort else None

    y1 = np.cos(theta)
    y2 = np.sin(theta)

    X = theta.reshape(-1, 1)
    Y = np.c_[y1, y2]
    Y += noise_scale * rng.randn(*Y.shape)
    
    return X, Y

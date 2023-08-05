import pytest

import numpy as np

from tensorflow.keras.initializers import RandomNormal, TruncatedNormal
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from gpflow.likelihoods import Gaussian
from gpflow.kernels import Matern52
from gpflow.inducing_variables import InducingPoints
from gpflow.covariances import Kuu, Kuf
from gpflow.config import default_jitter

from sklearn.datasets import load_diabetes
from gptk.datasets import make_regression

from gptk.gpflow.models.utils import (
    create_variational_loc,
    create_variational_scale
)


@pytest.fixture(params=range(5))
def seed(request):
    return request.param


@pytest.fixture
def random_state(seed):
    return np.random.RandomState(seed)


@pytest.fixture(params=[Matern52, ])
def kernel(request):
    return request.param()


@pytest.fixture(params=[64, ])
def n_train(request):
    return request.param


@pytest.fixture(params=[128, ])
def n_test(request):
    return request.param


# @pytest.fixture(params=[1, 32, 256])
@pytest.fixture(params=[1, 32,])
def n_inducing(request):
    return request.param


@pytest.fixture(params=[1, 5])
def input_dim(request):
    return request.param


@pytest.fixture(params=[1, 3])
def output_dim(request):
    return request.param


@pytest.fixture
def train_data(kernel, n_train, input_dim, output_dim, noise_variance, 
               random_state):

    X_train, Y_train = make_regression(kernel.K, n_train, input_dim, 
                                       output_dim, hidden_dim=None, 
                                       noise_variance=noise_variance,
                                       random_state=random_state)

    # feature_scaler = MinMaxScaler(feature_range=(-1, 1))
    # target_scaler = StandardScaler()
    # X_train = feature_scaler.fit_transform(X_train)
    # Y_train = target_scaler.fit_transform(Y_train)

    return X_train, Y_train


@pytest.fixture
def X_train(train_data):
    return train_data[0]


@pytest.fixture
def Y_train(train_data):
    return train_data[1]


@pytest.fixture
def X_test(n_test, input_dim, random_state):
    return random_state.randn(n_test, input_dim)


@pytest.fixture
def inducing_variable(n_inducing, input_dim, random_state):
    return InducingPoints(random_state.randn(n_inducing, input_dim))  # [M, D]


@pytest.fixture(params=[0.8, ])  # [1e+0, 1e-1, 5e+0]
def noise_variance(request):
    return request.param


@pytest.fixture
def likelihood(noise_variance):
    return Gaussian(variance=noise_variance)


@pytest.fixture(params=[False, True])
def q_diag(request):
    return request.param


@pytest.fixture(params=[False, True])
def diag_cov(request):
    return request.param


@pytest.fixture
def Kmm(inducing_variable, kernel):    
    return Kuu(inducing_variable, kernel, jitter=default_jitter())  # [M, M]


@pytest.fixture
def Kmn(inducing_variable, kernel, X_train):
    return Kuf(inducing_variable, kernel, X_train)  # [M, N]


@pytest.fixture
def Kmt(inducing_variable, kernel, X_test):
    return Kuf(inducing_variable, kernel, X_test)  # [M, N]


@pytest.fixture
def Ktt(kernel, X_test, diag_cov):
    return kernel(X_test, full_cov=not diag_cov)  # [T, T]


@pytest.fixture
def q_loc(output_dim, n_inducing, seed):
    q_loc_initializer = RandomNormal(stddev=1., seed=seed)
    return create_variational_loc(output_dim, n_inducing, q_loc_initializer)


@pytest.fixture
def q_scale_linop(output_dim, n_inducing, q_diag, seed):
    q_scale_initializer = TruncatedNormal(mean=1., seed=seed) if q_diag \
         else RandomNormal(seed=seed)
    return create_variational_scale(output_dim, n_inducing, q_diag,
                                    q_scale_initializer)

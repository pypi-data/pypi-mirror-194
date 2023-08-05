import numpy as np
import pandas as pd
import pyreadr

# from importlib.resources import files
from pathlib import Path
from sklearn.utils import Bunch


def load_jura(feature_columns=['long', 'lat'], 
              target_columns=["Cd", "Co", "Cr", "Cu", "Ni", "Pb", "Zn"]):

    """
    Swiss Jura mineral concentration dataset.

    Examples
    --------

    .. plot::
        :include-source:
        :context: close-figs

        from gptk.datasets import load_jura

        jura = load_jura()

        fig, ax = plt.subplots()

        ax.set_title('Zinc concentration')

        cbar = ax.scatter(*jura.data.T, c=jura.target[..., -1], cmap="crest", alpha=0.8)
        fig.colorbar(cbar, ax=ax)

        ax.set_xlabel('longitude')
        ax.set_ylabel('latitude')

        plt.show()    
    """

    # path = files('gptk.datasets.data').joinpath('snelson1d.npz')
    path = Path(__file__).parent.joinpath('data', 'jura.rda')

    frame = pyreadr.read_r(path).get('jura.pred')

    return Bunch(data=frame[feature_columns].to_numpy(), 
                 target=frame[target_columns].to_numpy())


def load_snelson_1d():

    # path = files('gptk.datasets.data').joinpath('snelson1d.npz')
    path = Path(__file__).parent.joinpath('data', 'snelson1d.npz')

    with np.load(path) as dataset:
        data = dataset['X']
        target = dataset['Y']

    return Bunch(data=data, target=target)


def load_motorcycle():

    """
    Motorcycle dataset.

    Examples
    --------

    .. plot::
        :include-source:
        :context: close-figs

        from gptk.datasets import load_motorcycle

        motorcycle = load_motorcycle()

        fig, ax = plt.subplots()

        ax.scatter(motorcycle.data, motorcycle.target, s=3.0, marker='o', color='k', alpha=0.8)

        ax.set_xlabel("times")
        ax.set_ylabel("acceleration")

        plt.show()
    """

    path = Path(__file__).parent.joinpath('data', 'motor.csv')
    frame = pd.read_csv(path, index_col=0)

    return Bunch(
        data=frame[["times"]].to_numpy(),
        target=frame[["accel"]].to_numpy(),
    )

import numpy as np

import matplotlib.pyplot as plt

from typing import Tuple, Union, TypeVar, Iterable, Dict

from goa import problems

T = TypeVar("T")


def plot_population(
    problem: problems.BaseProblem,
    X: Union[T, Iterable[T]],
    ax: plt.Axes = None,
    c: str = "darkblue",
    linestyle: str = ":",
    marker: str = "X",
    markersize: int = 6,
    markevery: int = 2,
    antialiased: bool = True,
    figsize: Tuple[float, float] = (12, 8),
    kwargs: Dict = None,
) -> plt.Axes:
    knobs = dict()
    if kwargs is not None:
        knobs.update(kwargs)
    if not ax:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(projection="3d")
    if X.shape == (2,):
        X = [X]
    for x, y in X:
        ax.plot(
            [x, x],
            [y, y],
            [problem(np.asarray([x, y])), 0],
            c=c,
            linestyle=linestyle,
            marker=marker,
            markersize=markersize,
            markevery=markevery,
            antialiased=antialiased,
            **knobs
        )
    return ax


def root_mean_squared_error(
    x: Union[float, np.ndarray], y: Union[float, np.ndarray]
) -> float:
    return np.sqrt(np.mean(np.power(np.subtract(x, y), 2)))


def custom_init_view_function(
    y: float = 20, x: float = 120, a: float = 30, b: float = 15
) -> Tuple[float, float]:
    return a - np.cos(y) * b, x

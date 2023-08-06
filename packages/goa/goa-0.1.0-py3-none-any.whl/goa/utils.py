import numpy as np

import matplotlib.pyplot as plt


def root_mean_squared_error(x, y) -> float:
    return np.sqrt(np.mean(np.power(np.subtract(x, y), 2)))


def custom_init_view_function(y=20, x=120):
    return 30 - np.cos(y) * 15, x


def plot_population(
    problem,
    X,
    ax=None,
    c="darkblue",
    linestyle=":",
    marker="X",
    markersize=6,
    markevery=2,
    antialiased=True,
    figsize=(12, 8),
    kwargs=None,
):
    knobs = dict()
    if kwargs is not None:
        knobs.update(kwargs)
    if not ax:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(projection="3d")
    if X.shape == (2, ):
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

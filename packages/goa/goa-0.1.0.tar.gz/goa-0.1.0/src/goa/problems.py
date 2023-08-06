import numpy as np
import matplotlib.pyplot as plt


class BaseProblem:
    def __init__(self, dim=1, bounds=(-1, 1), name=None):
        self.bounds = [bounds] * dim
        self.dim = dim
        self.name = name or self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)

    def evaluate(self, x):
        raise NotImplementedError("Implement the evaluation function.")

    def plot(
        self,
        ax=None,
        fig=None,
        figsize=(12, 8),
        num_points=100,
        background_color=(1.0, 1.0, 1.0, 0.0),  # white
        levels=100,
        cmap="Blues_r",
        alpha=0.75,
        offset=0.10,
        view_init=None,
    ):
        xbounds, ybounds = self.bounds[0], self.bounds[1]
        x = np.linspace(min(xbounds), max(xbounds), num_points)
        y = np.linspace(min(ybounds), max(ybounds), num_points)
        X, Y = np.meshgrid(x, y)
        grid = np.stack((X.flatten(), Y.flatten()), axis=-1)
        Z = np.apply_along_axis(self, 1, grid).reshape(X.shape)
        if ax and not fig:
            raise ValueError("Providing `ax` you should provide also `fig`")
        if not ax:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(projection="3d")
        xlim = (min(xbounds) * (1 + offset), max(xbounds) * (1 + offset))
        ylim = (min(ybounds) * (1 + offset), max(ybounds) * (1 + offset))
        if view_init:
            ax.view_init(*view_init)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.w_xaxis.set_pane_color(background_color)
        ax.w_yaxis.set_pane_color(background_color)
        ax.w_zaxis.set_pane_color(background_color)
        ax.plot_surface(
            X,
            Y,
            Z,
            cmap=cmap,
            alpha=alpha ** 4,
            antialiased=True,
            rstride=1,
            cstride=1,
            linewidth=0.1,
            edgecolors="black",
        )
        ax.contourf(
            X,
            Y,
            Z,
            cmap=cmap,
            alpha=alpha,
            antialiased=True,
            zdir="z",
            zorder=1,
            levels=levels,
            offset=np.min(Z),
        )
        return fig, ax


class Ackley(BaseProblem):
    def __init__(self, dim=2, bounds=(-32.768, 32.768), a=20, b=0.2, c=2 * np.pi):
        super().__init__(dim, bounds)
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, x):
        assert len(x) == self.dim
        s1 = np.sum(np.power(x, 2), axis=-1)
        s2 = np.sum(np.cos(self.c * x), axis=-1)
        return (
            -self.a * np.exp(-self.b * np.sqrt(s1 / self.dim))
            - np.exp(s2 / self.dim)
            + self.a
            + np.exp(1)
        )


class Rastrigin(BaseProblem):
    def __init__(self, dim=2, bounds=(-5.12, 5.12), a=10):
        super().__init__(dim, bounds)
        self.a = a

    def evaluate(self, x):
        return self.a * self.dim + np.sum(
            np.power(x, 2) - self.a * np.cos(2 * np.pi * x), axis=-1
        )


class Quadratic(BaseProblem):
    def __init__(self, dim=2, bounds=(-5, 5), Q=((1., 0.), (0., 1.)), b=(0., 0.), c=0.):
        super().__init__(dim, bounds)
        self.Q = np.asarray(Q)
        self.b = np.asarray(b)
        self.c = c

    def evaluate(self, x):
        assert len(x) == self.dim
        x = np.asarray(x)
        return 1/2 * np.dot(
            np.dot(np.transpose(x), self.Q),
            np.asarray(x)
        ) + np.dot(np.transpose(self.b), x) + self.c


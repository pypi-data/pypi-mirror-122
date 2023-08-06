import copy
import tempfile

from pathlib import Path

import imageio
import numpy as np

from matplotlib import animation
from goa import utils


def differential_evolution(
    problem,
    population_size: int = 10,
    problem_dim: int = 2,
    problem_bounds: tuple = None,
    F: float = 0.5,
    CR: float = 0.0,
    convergence_epsilon: float = 1e-4,
    max_iterations_without_improvement: int = 100,
    print_every: int = 5,
    animation_filepath: str = "",
) -> np.ndarray:
    """Differential Evolution algorithm.

    Args:
        problem: Problem to solve.
        population_size: Number of points to initialize the search.
        problem_dim: Problem dimension. It's overridden by `problem.dim`, if exists.
        problem_bounds: tuple (lower_constraint, upper_constraint) assuming all
            constraints equal for each axis.
        F: Real constant that belongs to the interval (0, 2).
        CR: Probability of crossover.
        convergence_epsilon: Threshold to define convergence of function values.
        max_iterations_without_improvement: Number of iterations allowed without seeing
            any improvement in the function values considering all the points in the
            population.
        print_every: Information about the running status of the algorithm will be
            printed every `print_every` steps.
        animation_filepath: An animation of the algorithm will be generated and saved in the
            provided `animation_filepath` filepath.
    Returns:
        A population of points that hopefully has reached the global minimum.

    """

    if problem.dim is not None:
        problem_dim = problem.dim
    if problem_bounds is None:
        bounds = problem.bounds
    else:
        bounds = [problem_bounds] * problem.dim

    ll, uu = bounds[0][0], bounds[0][1]  # assuming same constraints for each axis
    X = np.random.uniform(ll, uu, (population_size, problem_dim))
    if not "".__eq__(animation_filepath):
        Xs = [copy.deepcopy(X)]

    stopping_rule = StoppingRule(
        convergence_epsilon, max_iterations_without_improvement
    )
    step = DifferentialEvolutionStep(problem=problem, X=X, F=F, CR=CR)
    y = np.apply_along_axis(func1d=problem, axis=1, arr=X)

    iteration_counter = 0
    while not stopping_rule(y):
        iteration_counter += 1
        if iteration_counter % print_every == 0:
            print(
                "Iteration: {:4d} | RMSE: {:.8f}".format(
                    iteration_counter, utils.root_mean_squared_error(y, np.mean(y))
                )
            )
        X = next(step)
        y = np.apply_along_axis(func1d=problem, axis=1, arr=X)
        if not "".__eq__(animation_filepath):
            Xs.append(copy.deepcopy(X))
    print("Terminated at Iteration: {}".format(iteration_counter))

    if not "".__eq__(animation_filepath):

        def animate(i, problem, Xs):
            fig_suptitle = "Differential Evolution algorithm\n(Iteration #{})".format(i)
            if i == 0:
                utils.plot_population(problem, Xs[i], ax=ax)
                fig.suptitle(fig_suptitle, fontsize=14)
            else:
                ax.clear()
                problem.plot(
                    ax=ax, fig=fig, view_init=utils.custom_init_view_function(i)
                )
                utils.plot_population(problem, Xs[i], ax=ax)
                fig.suptitle(fig_suptitle, fontsize=14)

        fig, ax = problem.plot(view_init=utils.custom_init_view_function(0))
        anim = animation.FuncAnimation(
            fig,
            animate,
            fargs=(problem, Xs),
            frames=iteration_counter + 1,
            repeat=False,
        )

        animation_filepath = Path(animation_filepath)
        with tempfile.TemporaryDirectory(dir=".") as temp_dir_name:
            temp_dir_name = Path(temp_dir_name)
            temp_animation_filepath = temp_dir_name / (animation_filepath.stem + ".png")
            anim.save(temp_animation_filepath, writer="imagemagick")
            with imageio.get_writer(animation_filepath, mode="I", fps=1) as writer:
                for image_filepath in temp_dir_name.iterdir():
                    image = imageio.imread(image_filepath)
                    writer.append_data(image)
    return X


class DifferentialEvolutionStep:
    def __init__(
        self,
        problem,
        X,
        F: float = 0.5,
        CR: float = 0.2,
    ):
        self.problem = problem
        self.X = X
        self.F = F
        self.CR = CR

    def __next__(self):
        population_size = self.X.shape[0]
        for i in range(population_size):
            (k1, k2, k3, ii) = np.random.choice(
                a=range(population_size), size=4, replace=False  # True is feasible too
            )
            trial = self.X[k1] + self.F * (self.X[k2] - self.X[k3])
            for j in range(len(self.X[k1])):
                if j == ii:
                    continue
                if np.random.random() < self.CR:
                    trial[j] = self.X[i][j]
            if self.problem(trial) < self.problem(self.X[i]):
                self.X[i] = trial
        return self.X


def memetic_differential_evolution(
    problem,
    local_search_algorithm,
    local_search_algorithm_args: dict = None,
    population_size: int = 10,
    problem_dim: int = 2,
    problem_bounds: tuple = None,
    F: float = 0.5,
    CR: float = 0.0,
    convergence_epsilon: float = 1e-4,
    max_iterations_without_improvement: int = 100,
    print_every: int = 5,
    animation_filepath: str = "",
) -> np.ndarray:
    """Memetic Differential Evolution algorithm.

    Args:
        problem: Problem to solve.
        population_size: Number of points to initialize the search.
        local_search_algorithm: Local search algorithm to use that take at least two
            arguments, a problem and an starting point.
        local_search_algorithm_args: Arguments for the provided local search algorithm.
        problem_dim: Problem dimension. It's overridden by `problem.dim`, if exists.
        problem_bounds: tuple (lower_constraint, upper_constraint) assuming all
            constraints equal for each axis.
        F: Real constant that belongs to the interval (0, 2).
        CR: Probability of crossover.
        convergence_epsilon: Threshold to define convergence of function values.
        max_iterations_without_improvement: Number of iterations allowed without seeing
            any improvement in the function values considering all the points in the
            population.
        print_every: Information about the running status of the algorithm will be
            printed every `print_every` steps.
        animation_filepath: An animation of the algorithm will be generated and saved in the
            provided `animation_filepath` filepath.
    Returns:
        A population of points that hopefully has reached the global minimum.

    """

    if problem.dim is not None:
        problem_dim = problem.dim
    if problem_bounds is None:
        bounds = problem.bounds
    else:
        bounds = [problem_bounds] * problem.dim

    ll, uu = bounds[0][0], bounds[0][1]  # assuming same constraints for each axis
    X = np.random.uniform(ll, uu, (population_size, problem_dim))
    if not "".__eq__(animation_filepath):
        Xs = [copy.deepcopy(X)]

    stopping_rule = StoppingRule(
        convergence_epsilon, max_iterations_without_improvement
    )
    step = MemeticDifferentialEvolutionStep(
        problem=problem,
        X=X,
        local_search_algorithm=local_search_algorithm,
        local_search_algorithm_args=local_search_algorithm_args,
        F=F,
        CR=CR,
    )
    y = np.apply_along_axis(func1d=problem, axis=1, arr=X)

    iteration_counter = 0
    while not stopping_rule(y):
        iteration_counter += 1
        if iteration_counter % print_every == 0:
            print(
                "Iteration: {:4d} | RMSE: {:.8f}".format(
                    iteration_counter, utils.root_mean_squared_error(y, np.mean(y))
                )
            )
        X = step.__next__()
        y = np.apply_along_axis(func1d=problem, axis=1, arr=X)
        if not "".__eq__(animation_filepath):
            Xs.append(copy.deepcopy(X))
    print("Terminated at Iteration: {}".format(iteration_counter))

    if not "".__eq__(animation_filepath):

        def animate(i, problem, Xs):
            fig_suptitle = "Memetic Differential Evolution algorithm\n(Iteration #{})".format(i)
            if i == 0:
                utils.plot_population(problem, Xs[i], ax=ax)
                fig.suptitle(fig_suptitle, fontsize=14)
            else:
                ax.clear()
                problem.plot(
                    ax=ax, fig=fig, view_init=utils.custom_init_view_function(i)
                )
                utils.plot_population(problem, Xs[i], ax=ax)
                fig.suptitle(fig_suptitle, fontsize=14)

        fig, ax = problem.plot(view_init=utils.custom_init_view_function(0))
        anim = animation.FuncAnimation(
            fig,
            animate,
            fargs=(problem, Xs),
            frames=iteration_counter + 1,
            repeat=False,
        )

        animation_filepath = Path(animation_filepath)
        with tempfile.TemporaryDirectory(dir=".") as temp_dir_name:
            temp_dir_name = Path(temp_dir_name)
            temp_animation_filepath = temp_dir_name / (animation_filepath.stem + ".png")
            anim.save(temp_animation_filepath, writer="imagemagick")
            with imageio.get_writer(animation_filepath, mode="I", fps=1) as writer:
                for image_filepath in temp_dir_name.iterdir():
                    image = imageio.imread(image_filepath)
                    writer.append_data(image)
    return X


class MemeticDifferentialEvolutionStep:
    def __init__(
        self,
        problem,
        X,
        local_search_algorithm,
        local_search_algorithm_args=None,
        F: float = 0.5,
        CR: float = 0.2,
    ):
        self.problem = problem
        self.X = X
        self.local_search_algorithm = local_search_algorithm
        self.F = F
        self.CR = CR

        self.local_search_algorithm_args = dict()
        if local_search_algorithm_args is not None:
            self.local_search_algorithm_args.update(local_search_algorithm_args)

    def __next__(self):
        population_size = self.X.shape[0]
        for i in range(population_size):
            (k1, k2, k3, ii) = np.random.choice(
                a=range(population_size), size=4, replace=False  # True is feasible too
            )
            trial = self.X[k1] + self.F * (self.X[k2] - self.X[k3])
            for j in range(len(self.X[k1])):
                if j == ii:
                    continue
                if np.random.random() < self.CR:
                    trial[j] = self.X[i][j]
            trial = self.local_search_algorithm(
                self.problem, trial, **self.local_search_algorithm_args
            )
            if self.problem(trial) < self.problem(self.X[i]):
                self.X[i] = trial
        return self.X

def coordinate_method(
    problem,
    x0=(1., 1.),
    alpha0: float = 1.0,
    theta: float = 0.5,
    epsilon: float = 1e-4,
    max_iterations: int = 100,
    animation_filepath: str = "",
    view_init: tuple = (30, 120),
):
    alpha = alpha0
    x = np.asarray(x0)
    if not "".__eq__(animation_filepath):
        xs = [copy.deepcopy(x)]
        alphas = [copy.deepcopy(alpha)]
    n = 1 if len(x.shape) == 0 else x.shape[0]
    directions = np.append(np.eye(n), -1 * np.ones((1, n)), axis=0)
    step = CoordinateMethodStep(problem, x, alpha, theta, directions)

    iteration_counter = 0
    while not alpha < epsilon and iteration_counter < max_iterations:
        iteration_counter += 1
        x, alpha = step.__next__()
        if not "".__eq__(animation_filepath):
            xs.append(copy.deepcopy(x))
            alphas.append(copy.deepcopy(alpha))

    if not "".__eq__(animation_filepath):
        def animate(i, problem, xs, alphas, view_init):
            fig_suptitle = "Coordinate Method with Simple Descent Step\n(Iteration #{} | Alpha: {:.6f})".format(i, alphas[i])
            if i == 0:
                utils.plot_population(problem, xs[i], ax=ax)
                fig.suptitle(fig_suptitle, fontsize=14)
            else:
                ax.clear()
                problem.plot(ax=ax, fig=fig, view_init=view_init)
                utils.plot_population(problem, xs[i], ax=ax)
                fig.suptitle(fig_suptitle, fontsize=14)

        fig, ax = problem.plot(view_init=view_init)
        anim = animation.FuncAnimation(
            fig,
            animate,
            fargs=(problem, xs, alphas, view_init),
            frames=iteration_counter + 1,
            repeat=False,
        )

        animation_filepath = Path(animation_filepath)
        with tempfile.TemporaryDirectory(dir=".") as temp_dir_name:
            temp_dir_name = Path(temp_dir_name)
            temp_animation_filepath = temp_dir_name / (animation_filepath.stem + ".png")
            anim.save(temp_animation_filepath, writer="imagemagick")
            with imageio.get_writer(animation_filepath, mode="I", fps=1) as writer:
                for image_filepath in temp_dir_name.iterdir():
                    image = imageio.imread(image_filepath)
                    writer.append_data(image)
    return x


class CoordinateMethodStep:
    def __init__(self, problem, x, alpha, theta, directions):
        self.problem = problem
        self.x = x
        self.alpha = alpha
        self.theta = theta
        self.directions = directions

    def __next__(self):
        trials_y = np.asarray(
            [self.problem(self.x + self.alpha * d) for d in self.directions]
        )
        argmin_trials_y = np.argmin(trials_y)
        min_trials_y = trials_y[argmin_trials_y]
        y = self.problem(self.x)

        if min_trials_y < y:
            self.x = self.x + self.alpha * self.directions[argmin_trials_y]
        else:
            self.alpha = self.theta * self.alpha
        return self.x, self.alpha


class StoppingRule:
    """Return True if no change has been observed in `y` during the last
    `iteration_max` iterations of the algorithm.

    """

    def __init__(
        self,
        convergence_epsilon: float = 1e-7,
        max_iterations_without_improvement: int = 100,
    ):
        self.convergence_epsilon = convergence_epsilon
        self.max_iterations_without_improvement = max_iterations_without_improvement
        self.iteration_counter = -1
        self.y = None
        self.old_y = None

    def __call__(self, y) -> bool:
        self.y = y
        if self.first_stopping_rule():
            return True
        if self.old_y is None:
            self.old_y = self.y
        if self.second_stopping_rule():
            return True
        return False

    def first_stopping_rule(self) -> bool:
        mean_y = np.mean(self.y)
        rmse = utils.root_mean_squared_error(self.y, mean_y)
        if rmse < self.convergence_epsilon:
            return True
        return False

    def second_stopping_rule(self) -> bool:
        if np.allclose(self.old_y, self.y):
            self.iteration_counter += 1
        else:
            self.iteration_counter = 0
        if self.iteration_counter >= self.max_iterations_without_improvement:
            return True
        self.old_y = self.y
        return False

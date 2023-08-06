"""Console script for goa."""
import sys
import click
import matplotlib.pyplot as plt

from goa import problems, algorithms

algorithm_help = """
Optimization algorithm to solve the given problem.
"""
problem_help = """
 """
animation_filepath_help = """
An animation will be saved at the provided filepath location, if provided.\n
It should end with .gif extension.
"""

def float_tuple_type(text):
    text = str(text)
    text = text.replace('(', '').replace(')', '')
    (x, y) = list(map(float, text.split(',')))
    return (x, y)

@click.command()
@click.option(
    "--problem",
    prompt="Select a problem",
    default='Ackley',
    help='Choose the name of the problem to solve.',
    type=click.Choice(['Ackley', 'Rastrigin', 'quadratic'], case_sensitive=False),
)
@click.option(
    "--problem-bounds",
    prompt="[OPTIONAL] Change the problem bounds",
    default="(-2.5, 2.5)",
    type=float_tuple_type,
    help='Bounds for the given problem.',
)
@click.option(
    "--algorithm",
    prompt="Select an optimization algorithm",
    default='DE',
    type=click.Choice(['MDE', 'DE', 'CM'], case_sensitive=False),
    help=algorithm_help
)
@click.option(
    "--local-search-algorithm",
    prompt="[REQUIRED only with MDE] Select a local search algorithm",
    default="None",
    type=click.Choice(['CM', "None"], case_sensitive=False),
    help=animation_filepath_help,
)
@click.option(
    "--animation-filepath",
    default="",
    prompt="[OPTIONAL] Want an animation? Provide a filepath .gif",
    help=animation_filepath_help,
)

def main(
    problem,
    problem_bounds,
    algorithm,
    local_search_algorithm,
    animation_filepath
):
    problem_dict = {
        'ackley': problems.Ackley,
        'rastrigin': problems.Rastrigin,
        'quadratic': problems.Quadratic
    }
    algorithm_dict = {
        'MDE': algorithms.memetic_differential_evolution,
        'DE': algorithms.differential_evolution,
        'CM': algorithms.coordinate_method
    }
    animation_filepath = animation_filepath.strip("'")
    problem_instance = problem_dict[problem.lower()](bounds=problem_bounds)

    if not "None".__eq__(local_search_algorithm):
        algorithm_dict[algorithm.upper()](
            problem=problem_instance,
            local_search_algorithm=algorithm_dict[local_search_algorithm],
            animation_filepath=animation_filepath
        )
    else:
        algorithm_dict[algorithm.upper()](
            problem=problem_instance,
            animation_filepath=animation_filepath
        )

if __name__ == '__main__':
    sys.exit(main())

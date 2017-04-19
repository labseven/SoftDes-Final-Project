"""
Evolutionary algorithm, attempts to evolve a given message string.

Uses the DEAP (Distributed Evolutionary Algorithms in Python) framework,
http://deap.readthedocs.org

Usage:
    python evolve_text.py [goal_message]

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/evolutionary-algorithms
"""

import random

import numpy    # Used for statistics
from deap import algorithms
from deap import base
from deap import tools
import evolutionary_main

# -----------------------------------------------------------------------------
#  Global variables
# -----------------------------------------------------------------------------

VALID_COEFF = numpy.arange(-1, 1.1, 0.1)
# Control whether all Autopilots are printed as they are evaluated
VERBOSE = False


# ----------------------------------------------------------------------------
# Autopilot object to use in evolutionary algorithm
# -----------------------------------------------------------------------------

class FitnessMaximizeSingle(base.Fitness):
    """
    Class representing the fitness of a given individual, with a single
    objective that we want to minimize (weight = -1)
    """
    weights = (1.0, )


class Autopilot(list):
    """
    Representation of an individual Autopilot within the population to be evolved

    We represent the Autopilot as a list of coefficients (mutable) so it can
    be more easily manipulated by the genetic operators.
    """
    def __init__(self, initial_vals=-2):
        """
        Create a new Autopilot individual.

        If starting_string is given, initialize the Autopilot with the
        provided string message. Otherwise, initialize to a random string
        message with length between min_length and max_length.
        """
        # Want to minimize a single objective: distance from the goal message
        self.fitness = FitnessMaximizeSingle()

        # populate Autopilot with 20 random characters
        # print(initial_vals)
        if initial_vals is not -2:
            self.extend(initial_vals)
        initial_length = 20
        for i in range(initial_length):
            self.append(str(random.choice(VALID_COEFF)))

    def __repr__(self):
        """Return a string representation of the Autopilot"""
        # Note: __repr__ (if it exists) is called by __str__. It should provide
        #       the most unambiguous representation of the object possible, and
        #       ideally eval(repr(obj)) == obj
        # See also: http://stackoverflow.com/questions/1436703
        template = '{cls}({val!r})'
        return template.format(cls=self.__class__.__name__,     # "Autopilot"
                               val=self.get_text())

    def get_text(self):
        """Return Autopilot as string (rather than actual list of chars)"""
        try:
            return "".join(self)
        except(TypeError):
            return 'FAILED'


# -----------------------------------------------------------------------------
# Genetic operators
# -----------------------------------------------------------------------------


def evaluate_driving(message, verbose=VERBOSE):
    """
    Given a Autopilot and a goal_text string, return the Levenshtein distance
    between the Autopilot and the goal_text as a length 1 tuple.
    If verbose is True, print each Autopilot as it is evaluated.
    """

    file_object = open('Pilots.txt', 'a')
    file_object.write('\n' + message.get_text())
    file_object.close()

    pilot_instance = list(message)
    distance = evolutionary_main.main(True, False, pilot_instance)
    if verbose:
        print("{msg!s}\t[Distance: {dst!s}]".format(msg=message, dst=distance))
    return (distance, )     # Length 1 tuple, required by DEAP


def mutate_autopilots(coefficients, prob_sub=0.05):
    """
    Given a Autopilot and independent probabilities for each mutation type,
    return a length 1 tuple containing the mutated Autopilot.

    Possible mutations are:
        Substitution:   Replace one coefficients of the Autopilot with a random
                        (legal) coefficient

    >>> mutate_autopilots('hello', 1, 1, 1)
    """
    coefficients = list(coefficients)

    if random.random() < prob_sub:
        index = random.randint(0, len(coefficients) - 1)
        coefficients[index] = random.choice(VALID_COEFF)

    # message = ''.join(coefficients)
    # print('mutated: ', message)

    return(Autopilot(coefficients), )   # Length 1 tuple, required by DEAP


# -----------------------------------------------------------------------------
# DEAP Toolbox and Algorithm setup
# -----------------------------------------------------------------------------

def get_toolbox():
    """Return DEAP Toolbox configured to evolve given 'text' string"""

    # The DEAP Toolbox allows you to register aliases for functions,
    # which can then be called as "toolbox.function"
    toolbox = base.Toolbox()

    # Creating population to be evolved
    toolbox.register("individual", Autopilot)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Genetic operators
    toolbox.register("evaluate", evaluate_driving)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_autopilots)
    toolbox.register("select", tools.selTournament, tournsize=5)

    # NOTE: You can also pass function arguments as you define aliases, e.g.
    #   toolbox.register("individual", Autopilot, max_length=200)
    #   toolbox.register("mutate", mutate_autopilots, prob_sub=0.18)

    return toolbox


def evolve_autopilot():
    """Use evolutionary algorithm (EA) to evolve 'text' string"""

    # Set random number generator initial seed so that results are repeatable.
    # See: https://docs.python.org/2/library/random.html#random.seed
    #      and http://xkcd.com/221
    # random.seed(6)

    # Get configured toolbox and create a population of random Autopilots
    toolbox = get_toolbox()
    pop = toolbox.population(n=20)
    # Collect statistics as the EA runs
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    hof = tools.HallOfFame(5)
    print(hof)
    # Run simple EA
    # (See: http://deap.gel.ulaval.ca/doc/dev/api/algo.html for details)
    pop, log = algorithms.eaSimple(pop,
                                   toolbox,
                                   0.5,    # Prob. of crossover (mating)
                                   0.8,   # Probability of mutation
                                   50,    # Num. of generations to run
                                   stats,
                                   hof)

    print(hof)
    return pop, log


# -----------------------------------------------------------------------------
# Run if called from the command line
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Run evolutionary algorithm
    pop, log = evolve_autopilot()

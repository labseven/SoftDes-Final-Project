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

d = {}
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
        else:
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
        string = ''
        length = len(self)
        for i, coef in enumerate(self):
            if i == 0:
                try:
                    string += '\n(' + str(coef) + ', '
                except(TypeError):
                    string += '\n(' + coef.astype('|S10') + ', '
            elif i == length - 1:
                try:
                    string += str(coef) + ')'
                except(TypeError):
                    string += coef.astype('|S10') + ')'
            else:
                try:
                    string += str(coef) + ', '
                except(TypeError):
                    string += coef.astype('|S10') + ')'
        # print(string)
        return string

# -----------------------------------------------------------------------------
# Genetic operators
# -----------------------------------------------------------------------------


def evaluate_driving(message, verbose=VERBOSE):
    """
    Given a Autopilot and a goal_text string, return the Levenshtein distance
    between the Autopilot and the goal_text as a length 1 tuple.
    If verbose is True, print each Autopilot as it is evaluated.
    """
    # print('.'),
    mem = False
    try:
        distance = d[message.get_text()]
        mem = True
    except(KeyError):
        distance = evolutionary_main.main(True, False, message)
        d[message.get_text()] = distance
    # print(mem)
    file_object = open('Pilots.txt', 'a')
    file_object.write('\n' + (str)(distance) + str(mem) + ':' + message.get_text())
    file_object.close()

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
    toolbox.register("select", tools.selTournament, tournsize=3)

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

    pop = toolbox.population(n=200)
    # Collect statistics as the EA runs
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    hof = tools.HallOfFame(5)
    # Run simple EA
    # (See: http://deap.gel.ulaval.ca/doc/dev/api/algo.html for details)
    pop, log = algorithms.eaSimple(pop,
                                   toolbox,
                                   0.5,    # Prob. of crossover (mating)
                                   0.8,   # Probability of mutation
                                   40,    # Num. of generations to run
                                   stats,
                                   hof)

    print(hof)
    return pop, log


# -----------------------------------------------------------------------------
# Run if called from the command line
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # coef = '0.2-0.5-0.31.0-0.30.5-2.22044604925e-16-0.5-0.10.50.7-0.30.9-2.22044604925e-16-0.70.40.5-0.3-2.22044604925e-160.3-0.30.5-0.60.7-0.2-1.0-0.40.8-0.8-0.6-0.70.6-0.40.5-0.3-0.5-0.8-0.30.80.30.3-2.22044604925e-160.80.90.7-1.0-0.70.10.40.8-0.5-0.40.3-0.9-0.50.6-2.22044604925e-160.7-0.6-0.31.00.8-0.90.1-0.3-0.40.3-1.0-0.50.80.7-0.9-0.6-0.80.20.40.1-0.3-0.60.6-1.00.30.40.40.80.40.80.60.30.3-1.0-0.90.40.5-0.90.9-0.3-0.30.6-0.6-0.2-0.9-0.10.3-0.1-0.10.8-0.50.70.9-0.3-0.10.6-0.1-0.6-0.9-0.50.9-0.20.50.90.60.2-0.40.6-0.3-0.1-0.6-2.22044604925e-160.3-0.1-0.6-0.8-0.4-0.3-0.3-0.5-0.10.4-1.00.4-0.6-0.5-0.10.30.50.70.7-0.71.0-0.20.6-0.3-2.22044604925e-160.60.90.2-0.2-0.7-0.50.40.6-0.6-0.61.0-0.80.8-0.5-2.22044604925e-16-0.8-0.1-0.30.8-0.60.2-0.6-0.40.6-0.40.1-1.0-0.30.80.6-0.30.20.9-0.4-0.21.00.4-0.5-0.3-0.80.50.3-0.6-0.80.20.10.5-0.3-0.40.70.5-0.30.90.30.9-0.6-0.7-0.40.70.4-0.6-0.70.2-0.4-0.30.7-0.70.9-0.10.1-0.2-0.4-0.7-0.50.5-0.5-0.1-0.90.20.20.3-2.22044604925e-160.30.9-0.20.10.80.80.90.8-0.60.30.7-0.6-2.22044604925e-16-2.22044604925e-16-0.31.0-0.8-0.8-1.01.0-0.70.90.8-0.50.30.3-0.80.5-0.3-0.20.7-0.20.10.4-0.2-0.4-0.7-0.51.00.20.8-0.1-0.30.8'
    # Run evolutionary algorithm)
    # print(coef)
    """ WINNERS: CIRCLE TRACK"""
    # print(evaluate_driving(Autopilot((-0.6, -0.6, 0.4, 0, -0.6, -0.7, -0.8, -0.2, -0.3, 0.1, -1.0, 0.6, 0.6, -0.2, -0.9, 0.3, -0.6, 0.5, -0.4, -0.6))))  # 0.3, -0.3, 0.8, -0.7, 0.2, -0.7, 0.4, -0.2, 0.9, 0.9, 0.7, 0.8, -2.22044604925e-16, 0.4, -0.1, -0.5, 0.2, -0.5, 0.4, -0.2, -2.22044604925e-16, 0.2, 0.2, 0.6, 0.3, 0.9, -2.22044604925e-16, 0.9, 0.4, 0.5, 0.9, 0.4, -0.3, -0.5, 0.1, -0.3, -2.22044604925e-16, -2.22044604925e-16, -0.4, -0.5, 0.6, 0.8, -0.8, 0.7, -0.7, 0.6, 0.7, 0.5, -0.2, -0.3, -2.22044604925e-16, -0.3, -0.3, 0.2, 0.9, 0.6, -0.7, -0.4, 0.7, 0.6, -2.22044604925e-16, 0.8, 0.7, -0.6, 0.1, -0.7, -0.1, 0.3, -2.22044604925e-16, 0.1, -0.5, -0.3, 1.0, 0.6, 0.2, -1.0, 0.3, -0.7, 0.1, 0.5, 0.8, -0.6, 0.3, -0.3, -1.0, -1.0, 0.3, -0.5, 1.0, 0.7, 0.6, 0.5, -0.6, 0.7, 0.7, 0.2, -0.3, -1.0, 0.7, -1.0, -0.6, 0.8, 0.4, 0.5, -0.4, -0.5, -0.9, 0.7, -0.4, -0.3, 0.1, 0.5, 0.3, 0.5, -2.22044604925e-16, -0.7, -1.0, 0.9, 1.0, 1.0, 0.2, -0.4, 0.7, 0.7, -0.8, 1.0, -0.3, -0.4, -0.4, 0.6, 0.7, 0.7, 0.2, -0.2, 0.7, 0.2, -0.7, 0.9, -0.4, -0.6, 1.0, 0.2, -0.6, 1.0, 0.6, -0.1, -0.6, 0.7, 0.6, -1.0, -0.1, 0.5, 0.4, -0.3, -0.8, -0.3, 0.1, -0.7, 1.0, -0.8, -0.4, -1.0, 0.3, -0.1, 0.1, -0.7, -0.4, -0.4, -2.22044604925e-16, 0.4, -0.4, 0.3, -0.1, -0.8, 0.3, -0.1, 0.9, -0.3, -0.7, -2.22044604925e-16, -0.8, 0.6, -0.5, -1.0, 0.2, -0.2, -0.5, 0.5, -0.2, 0.8, -0.6, 0.4, -2.22044604925e-16, 0.5, -0.8, 0.9, -0.1, 0.8, 0.2, 0.8, -0.2, -0.5, -0.9, 1.0, -0.7, -0.7, 0.9, -0.5, 0.1, 0.6, -0.4, -2.22044604925e-16, 0.1, -0.5, 0.6, -0.8, -0.7, 0.3, -0.5, -1.0, -0.6, -0.5, -0.4, -0.4, 0.4, -0.3, 0.2, 0.4, -0.9, 1.0, -0.8, 0.6, -0.4, 0.2, -0.5, -1.0, -0.5, -1.0, -0.4, -0.5)))
    # print(evaluate_driving(Autopilot((0.3, -0.6, 0.4, -0.5, 0.6, -0.7, -0.8, -0.2, -0.3, 0.1, -1.0, 0.6, 0.6, -0.2, -0.9, 0.3, -0.6, 0.5, -0.4, -0.6, 0.3))))
    """WINNERS: Chris Track"""
    # print(evaluate_driving(Autopilot((-0.5, 0.8, -0.5, -0.4, -0.3, -0.6, -0.2, 0.4, -2.22044604925e-16, -0.9, -1.0, -0.6, 0.2, 0.5, -1.0, -2.22044604925e-16, 0.8, -0.8, -0.7, 0.5))))
    # print(evaluate_driving(Autopilot((0.3, -1.0, -0.5, 0.8, -0.3, 0.3, 0.5, -0.6, 0.4, -0.4, 0.2, -0.2, 0.7, 0.5, -1.0, -2.22044604925e-16, -0.9, 1.0, -0.3, -0.9))))
    print(evaluate_driving(Autopilot((0.6, 0.4, -0.1, -0.3, -0.5, 0.5, -0.5, 0.8, -0.7, -0.8, -0.2, -0.7, -0.3, 1.0, 0.3, -0.7, -0.9, -0.4, 1.0, -1.0))))
    # pop, log = evolve_autopilot()

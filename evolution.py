"""
Highest-Level script to be called when running evolution.

@author Alex Chapman
(c) April 2017
Evolutionary algorithm, attempts to evolve a given message string.

Uses the DEAP (Distributed Evolutionary Algorithms in Python) framework,
http://deap.readthedocs.org

Usage:
    python evolution.py

Full instructions will be on github shortly.
"""

import random
import numpy    # Used for statistics
from deap import algorithms
from deap import base
from deap import tools
import evolutionary_main
import tkinter as tk
from tkinter import *
import pickle

# -----------------------------------------------------------------------------
#  Global variables
# -----------------------------------------------------------------------------
MAP_NAME = 'Clover_track'

# Establish a list of coefficients for the mutation method to insert into the genome
VALID_COEFF = numpy.arange(-1, 1.1, 0.1)
# Control whether all Autopilots are printed as they are evaluated
VERBOSE = False

# Dictionary for memoization
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

    represent the Autopilot as a list of coefficients (mutable) so it can
    be more easily manipulated by the genetic operators.
    """
    def __init__(self, initial_vals=None):
        """
        Create a new Autopilot individual.

        If starting_string is given, initialize the Autopilot with the
        provided string message. Otherwise if -2, initialize to a random string
        message with length between min_length and max_length.
        """
        # Want to minimize a single objective: distance from the goal message
        self.fitness = FitnessMaximizeSingle()

        # populate Autopilot with 20 random characters as long as no  precedent exists
        if initial_vals is not None:
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
        """Return Autopilot as string, accounting for float vs integer quantities,
        output is of the format:

        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        """
        string = ''
        length = len(self)
        for i, coef in enumerate(self):
            # if self is the first in the list
            if i == 0:
                try:
                    # only works if coef is not float
                    string += '\n(' + str(coef) + ', '
                except(TypeError):
                    # truncates value should coefficient be a float and in the beginning of the array
                    string += '\n(' + coef.astype('|S10') + ', '
            elif i == length - 1:
                # string at the end of the list of coefficients
                try:
                    string += str(coef) + ')'
                except(TypeError):
                    # or float
                    string += coef.astype('|S10') + ')'
            else:
                try:
                    # truncates value should coefficient be a float and in the end of the array
                    string += str(coef) + ', '
                except(TypeError):
                    string += coef.astype('|S10') + ')'
        # print(string)
        return string

# -----------------------------------------------------------------------------
# Genetic operators
# -----------------------------------------------------------------------------


def evaluate_driving(auto, draw=False, verbose=VERBOSE, map_name=MAP_NAME, memoize=True):
    """
    Given a Autopilot and a map, return the  distance The autopilot makes
    as a length 1 tuple. If verbose is True, print each Autopilot as it is evaluated.
    map_name may be one of four valid track names:
    Clover_track
    Circle_Track
    Chris_Track
    Tri-Clover
    If additional track folders are added to the folder they can be referenced as well.
    """
    # memoiziation
    mem = False
    if memoize:
        # disabled for the show of runnning multiple autopilots on different maps
        try:
            distance = d[auto.get_text()]
            mem = True
        except(KeyError):
            # only happens of memoization is off or if autopilot is not in existing dictionary
            distance = evolutionary_main.main(draw, False, auto, map_name)
            d[auto.get_text()] = distance
    else:
        # if memoization is not active, run as normal
        # FORMAT IS  draw (boolean), Control (Boolean), auto (Autopilot), map_name (String)
        distance = evolutionary_main.main(draw, False, auto, map_name)
    # pickle to save each autopilot to the master record "Pilots.txt" file
    file_object = open('Pilots.txt', 'a')
    file_object.write('\n\n' + (str)(distance) + '\t' + str(mem) + '\t' + map_name + ':' + auto.get_text())
    file_object.close()

    if verbose:
        print("{msg!s}\t[Distance: {dst!s}]".format(msg=auto, dst=distance))
    return (distance, )     # Length 1 tuple, required by DEAP


def mutate_autopilots(coefficients, prob_sub=0.05):
    """
    Given a Autopilot and independent probabilities for the mutation type,
    return a length 1 tuple containing the mutated Autopilot.

    Possible mutation is:
        Substitution:   Replace one coefficients of the Autopilot with a random
                        (legal) coefficient

    """
    coefficients = list(coefficients)

    if random.random() < prob_sub:
        index = random.randint(0, len(coefficients) - 1)
        coefficients[index] = random.choice(VALID_COEFF)

    return(Autopilot(coefficients), )   # Length 1 tuple, required by DEAP


# -----------------------------------------------------------------------------
# DEAP Toolbox and Algorithm setup
# CREDIT: SoftDes 2017 Professors.
# https://github.com//sd17spring/ToolBox-EvolutionaryAlgorithms
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

    # Get configured toolbox and create a population of random Autopilots
    toolbox = get_toolbox()

    pop = toolbox.population(n=300)
    # Collect statistics as the EA runs
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Added Hall of Fame functionality to save best autopilots
    hof = tools.HallOfFame(5)
    # Run simple EA
    # (See: http://deap.gel.ulaval.ca/doc/dev/api/algo.html for details)
    pop, log = algorithms.eaSimple(pop,
                                   toolbox,
                                   0.5,    # Prob. of crossover (mating)
                                   0.8,   # Probability of mutation
                                   200,    # Num. of generations to run
                                   stats,
                                   hof)

    print(hof)

    return pop, log, hof


def create_window():
    """
    Used to create UI popups that appear between runs of the Autopilots.
    Built using Tkinter tutorials mainly on stack overflow.
    """
    #Create buttons and labels
    def button1(event):
        to_return = 'Circle_Track'
        # Dumps the name of the map to pickle for cross-function access
        pickle.dump(to_return, open('map_name.p', 'wb'))
        root.destroy()

    def button2(event):
        to_return = 'Clover_track'
        # Dumps the name of the map to pickle for cross-function access
        pickle.dump(to_return, open('map_name.p', 'wb'))
        root.destroy()

    def button3(event):
        to_return = 'Chris_Track'
        # Dumps the name of the map to pickle for cross-function access
        pickle.dump(to_return, open('map_name.p', 'wb'))
        root.destroy()

    def button4(event):
        to_return = "Tri-Clover"
        # Dumps the name of the map to pickle for cross-function access
        pickle.dump(to_return, open('map_name.p', 'wb'))
        root.destroy()

    # Centers the window on the screen
    def center(toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    # Creates a window named root
    root = tk.Tk()
    # Initializes a text box
    T = Text(root, height=2, width=55)
    # Centers the box and the text within
    T.tag_configure("center", justify='center')
    # adds text to the text box
    T.insert(END, "The Simulation will run with pre-existing Autopilots.\nSelect which map they're run on!\n")
    # implements the centering
    T.tag_add("center", "1.0", "end")

    # officially adds all components to the window
    # Adds labels to buttons and resizes window slightly
    T.pack()
    b1 = tk.Button(root, text="Circle")
    b1.pack()
    b2 = tk.Button(root, text="Four-Leafed Clover")
    b2.pack()
    b3 = tk.Button(root, text="C-Shape")
    b3.pack()
    b4 = tk.Button(root, text="Tri-Clover")
    b4.pack()
    back = tk.Frame(master=root, width=255, height=45)
    back.pack()

    # names and centers window
    root.title("Choose Your Map")
    center(root)

    # binds buttons to their command functions
    b1.bind("<Button-1>", button1)
    b2.bind("<Button-1>", button2)
    b3.bind("<Button-1>", button3)
    b4.bind("<Button-1>", button4)
    root.mainloop()


# -----------------------------------------------------------------------------
# Run if called from the command line
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        map_to_use = 'test'
        # Opens popup window with choice of map_to_use
        create_window()
        # Access map name data generated by the interactive popup UI window
        map_to_use = pickle.load(open("map_name.p", "rb"))
        # """ WINNERS: CIRCLE TRACK"""
        # print(evaluate_driving(Autopilot((0.3, -0.6, 0.4, -0.5, 0.6, -0.7, -0.8, -0.2, -0.3, 0.1, -1.0, 0.6, 0.6, -0.2, -0.9, 0.3, -0.6, 0.5, -0.4, -0.6, 0.3)), True))
        #"""WINNERS: Chris Track"""
        # print(evaluate_driving(Autopilot((-0.5, 0.8, -0.5, -0.4, -0.3, -0.6, -0.2, 0.4, -2.22044604925e-16, -0.9, -1.0, -0.6, 0.2, 0.5, -1.0, -2.22044604925e-16, 0.8, -0.8, -0.7, 0.5)), True))
        # print(evaluate_driving(Autopilot((0.3, -1.0, -0.5, 0.8, -0.3, 0.3, 0.5, -0.6, 0.4, -0.4, 0.2, -0.2, 0.7, 0.5, -1.0, -2.22044604925e-16, -0.9, 1.0, -0.3, -0.9)), True))
        # """FOR SPEED"""
        # # print(evaluate_driving(Autopilot((0.6, 0.4, -0.1, -0.3, -0.5, 0.5, -0.5, 0.8, -0.7, -0.8, -0.2, -0.7, -0.3, 1.0, 0.3, -0.7, -0.9, -0.4, 1.0, -1.0)), True))
        # # print(evaluate_driving(Autopilot((-0.7, 0.8, 0.3, -0.7, -0.6, -0.9, 0.2, 0.6, -0.9, -0.7, -0.4, -0.2, 0.1, 0.9, -0.7, -0.3, -0.9, -0.9, 0.1, 0.5)), True))
        # """WINNERS: CLOVER TRACK"""

        print(evaluate_driving(Autopilot((0.9, -1.0, -0.6, 0.9, 0.7, -0.2, 0.6, -0.6, 0.2, 0.5, 0.9, 0.5, -0.2, -2.22044604925e-16, -0.9, 1.0, -0.1, 0.1, 1.0, -0.3)), True, map_name=map_to_use, memoize=False))
        # print(evaluate_driving(Autopilot((-0.5, -0.2, 0.3, -0.1, -0.5, -0.9, 1.0, 0.3, 0.1, -0.9, -0.1, -0.7, 0.9, 0.2, -0.7, 0.7, -0.4, 0.8, 0.5, 1.0)), True))
        # print(evaluate_driving(Autopilot((0.1, -1.0, -0.6, 0.8, 0.1, 0.4, -0.6, -0.3, -0.6, -0.4, -0.7, 0.8, -0.4, -0.2, 0.5, 0.6, -0.5, 0.1, -0.1, 0.2)), True))
        # clover track 10.4 (0.6, -0.7, -0.5, 1.0, -0.7, 1.0, 0.5, -0.7, 0.2, 0.2, 0.9, 0.3, 0.2, -1.0, -0.1, 0.3, -2.22044604925e-16, 0.5, 0.1, 0.6)
        # clover track 15.6 (0.7, -0.3, -1.0, 0.8, -0.4, 0.6, 0.7, -1.0, 0.7, 0.8, 0.6, 0.3, -2.22044604925e-16, -0.3, -0.7, 0.9, 0.3, 0.7, 0.7, -0.9)
        print(evaluate_driving(Autopilot((0.6, -0.7, -0.5, 1.0, -0.7, 1.0, 0.5, -0.7, 0.2, 0.2, 0.9, 0.3, 0.2, -1.0, -0.1, 0.3, -2.22044604925e-16, 0.5, 0.1, 0.6)), True, map_name=map_to_use, memoize=False))
        print(evaluate_driving(Autopilot((0.7, -0.3, -1.0, 0.8, -0.4, 0.6, 0.7, -1.0, 0.7, 0.8, 0.6, 0.3, -2.22044604925e-16, -0.3, -0.7, 0.9, 0.3, 0.7, 0.7, -0.9)), True, map_name=map_to_use, memoize=False))

        # used for rapid iterative evolution of autopilots.
        # pop, log, hof = evolve_autopilot()
        # file_object = open('BoTb.txt', 'a')
        # file_object.write(str(hof))
        # file_object.close()

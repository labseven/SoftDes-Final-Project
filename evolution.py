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
import os

# -----------------------------------------------------------------------------
#  Global variables
# -----------------------------------------------------------------------------
MAP_NAME = 'Clover_track'
EVOLVING = False
# Establish a list of coefficients for the mutation method to insert into the genome
VALID_COEFF = numpy.arange(-1, 1.1, 0.001)
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

        If initial_vals is given, initialize the Autopilot with the
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


def evaluate_driving(auto, draw=True, verbose=VERBOSE, map_name=MAP_NAME, memoize=True, control=False):
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
    if EVOLVING:
        memoize = True
        draw = False
    if memoize:
        # disabled for the show of runnning multiple autopilots on different maps
        try:
            distance = d[auto.get_text()]
            mem = True
        except(KeyError):
            # only happens of memoization is off or if autopilot is not in existing dictionary
            distance = evolutionary_main.main(draw, control, auto, map_name)
            d[auto.get_text()] = distance
    else:
        # if memoization is not active, run as normal
        # FORMAT IS  draw (boolean), Control (Boolean), auto (Autopilot), map_name (String)
        distance = evolutionary_main.main(draw, control, auto, map_name)
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

    pop = toolbox.population(n=10)
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
                                   10,    # Num. of generations to run
                                   stats,
                                   hof)

    print(hof)

    return pop, log, hof


def create_start_window():
    """
    Used to create UI popups that appear between runs of the Autopilots.
    Built using Tkinter tutorials mainly on stack overflow.
    """
    state = [None, -1]

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

    T = Text(root, height=2, width=35)  # Initializes a text box
    T.tag_configure("center", justify='center')  # Centers the box and the text within
    T.insert(END, "Select which map the simulation is run on!")  # adds text to the text box
    T.tag_add("center", "1.0", "end")  # implements the centering

    R = Text(root, height=2, width=16)
    R.tag_configure("center", justify='center')  # Centers the box and the text within
    R.insert(END, "Choose how the\n car drives!")  # adds text to the text box
    R.tag_add("center", "1.0", "end")  # implements the centering

    # Method that gets called on button push
    def sel(reset=False):
        # Dictionary for printing track selected name
        d = {1: 'Circle_Track', 2: 'Clover_track', 3: 'Chris_Track', 4: 'Tri-Clover', 5: None}
        try:
            print("You selected the option " + str(d[var1.get()]) + ':' + str(var2.get()))
        except:
            pass
        state[0] = str(d[var1.get()])
        state[1] = str(var2.get())

        # if both buttons are pushed, save states to pickle file.
        # if state[0] is not None and state[1] != '0':
        if reset:
            pickle.dump(state, open('map_name.p', 'wb'))
            root.destroy()

    var1 = IntVar()

    b1 = tk.Radiobutton(root, text="Circle", variable=var1, value=1, command=sel)
    b2 = tk.Radiobutton(root, text="Four-Leafed Clover", variable=var1, value=2, command=sel)
    b3 = tk.Radiobutton(root, text="C-Shape", variable=var1, value=3, command=sel)
    b4 = tk.Radiobutton(root, text="Tri-Clover", variable=var1, value=4, command=sel)
    b5 = tk.Radiobutton(root, text="Make Your Own", variable=var1, value=5, command=sel)

    T.grid(row=0, column=0, sticky=tk.W+tk.E)
    b1.grid(row=1, column=0, sticky=tk.W+tk.E)
    b2.grid(row=2, column=0, sticky=tk.W+tk.E)
    b3.grid(row=3, column=0, sticky=tk.W+tk.E)
    b4.grid(row=4, column=0, sticky=tk.W+tk.E)
    b5.grid(row=5, column=0, sticky=tk.W+tk.E)

    var2 = IntVar()
    R1 = Radiobutton(root, text="Existing Autonomous", variable=var2, value=2, command=sel)
    R2 = Radiobutton(root, text="Evolve New Autonomous", variable=var2, value=1, command=sel)
    R3 = Radiobutton(root, text="Drive it Yourself", variable=var2, value=3, command=sel)

    var3 = IntVar()
    b = Button(root, text="SUBMIT", command=lambda: sel(True))

    R.grid(row=0, column=1, sticky=tk.W+tk.E)
    R1.grid(row=1, column=1, sticky=tk.W+tk.E)
    R2.grid(row=2, column=1, sticky=tk.W+tk.E)
    R3.grid(row=3, column=1, sticky=tk.W+tk.E)
    b.grid(row=5, column=1, sticky=tk.W+tk.E)
    # names and centers window
    root.resizable(width=False, height=False)

    root.title("Choose Your Map")
    center(root)

    root.mainloop()

# -----------------------------------------------------------------------------
# Run if called from the command line
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        map_to_use = 'test'
        # Opens popup window with choice of map_to_use
        create_start_window()
        # Access map name data generated by the interactive popup UI window
        map_to_use, autopilot_style = pickle.load(open("map_name.p", "rb"))
        # """ WINNERS: CIRCLE TRACK"""
        # print(evaluate_driving(Autopilot((0.3, -0.6, 0.4, -0.5, 0.6, -0.7, -0.8, -0.2, -0.3, 0.1, -1.0, 0.6, 0.6, -0.2, -0.9, 0.3, -0.6, 0.5, -0.4, -0.6, 0.3)), True, map_name=map_to_use, memoize=False))

        # """WINNERS: Chris Track"""
        # print(evaluate_driving(Autopilot((-0.5, 0.8, -0.5, -0.4, -0.3, -0.6, -0.2, 0.4, 0.0, -0.9, -1.0, -0.6, 0.2, 0.5, -1.0, 0.0, 0.8, -0.8, -0.7, 0.5)), True, map_name=map_to_use, memoize=False))

        # """WINNERS: CLOVER TRACK"""
        # print(evaluate_driving(Autopilot((0.9, -1.0, -0.6, 0.9, 0.7, -0.2, 0.6, -0.6, 0.2, 0.5, 0.9, 0.5, -0.2, 0.0, -0.9, 1.0, -0.1, 0.1, 1.0, -0.3)), True, map_name=map_to_use, memoize=False))
        # print(evaluate_driving(Autopilot((0.6, -0.7, -0.5, 1.0, -0.7, 1.0, 0.5, -0.7, 0.2, 0.2, 0.9, 0.3, 0.2, -1.0, -0.1, 0.3, 0.0, 0.5, 0.1, 0.6)), True, map_name=map_to_use, memoize=False))
        # print(evaluate_driving(Autopilot((0.7, -0.3, -1.0, 0.8, -0.4, 0.6, 0.7, -1.0, 0.7, 0.8, 0.6, 0.3, 0.0, -0.3, -0.7, 0.9, 0.3, 0.7, 0.7, -0.9)), True, map_name=map_to_use, memoize=False))

        if autopilot_style == '2' or autopilot_style == '3':
            EVOLVING = False
            control_style = autopilot_style == '3'
            if control_style:
                evaluate_driving(Autopilot(), True, map_name=map_to_use, memoize=False, control=control_style)
            else:
                # print(evaluate_driving(Autopilot((-0.3, -0.3, -1.0, 0.8, -0.4, 0.6, 0.7, -1.0, 0.7, 0.8, 0.6, 0.3, 0.0, -0.3, -0.7, 0.9, 0.3, 0.7, 0.7, -0.9)), True, map_name=map_to_use, memoize=False, control=control_style))
                print(evaluate_driving(Autopilot((0.7, -0.3, -1.0, 0.8, -0.4, 0.6, 0.7, -1.0, 0.7, 0.8, 0.6, 0.3, 0.0, -0.3, -0.7, 0.9, 0.3, 0.7, 0.7, -0.9)), True, map_name=map_to_use, memoize=False, control=control_style))
                # 13
                print(evaluate_driving(Autopilot((-0.836, -0.925, -0.694, 0.467, 0.707, 0.616, 0.907, -0.245, 0.537, -0.431, 0.717, -0.085, 0.526, -0.315, 0.306, 0.384, -0.729, 1.052, 0.356, -0.352)), True, map_name=map_to_use, memoize=False, control=control_style))
                # 11.9
                print(evaluate_driving(Autopilot((-0.9, -0.925, -0.694, 0.467, 0.707, 0.616, 0.907, -0.245, 0.537, -0.431, 0.791, -0.085, 0.526, -0.315, 0.306, 0.384, -0.729, 1.052, 0.356, -0.352)), True, map_name=map_to_use, memoize=False, control=control_style))
                # 11.5
                print(evaluate_driving(Autopilot((-0.9, -0.587, -0.694, 0.467, 0.707, 0.616, 0.907, -0.245, 0.537, -0.431, 0.912, -0.085, 0.526, -0.315, 0.306, 0.384, -0.729, 1.052, 0.356, -0.352)), True, map_name=map_to_use, memoize=False, control=control_style))
        # used for rapid iterative evolution of autopilots.
        else:
            MAP_NAME = map_to_use
            EVOLVING = False
            pop, log, hof = evolve_autopilot()
            file_object = open('BoTb.txt', 'a')
            file_object.write(str(hof))
            file_object.close()
        if map_to_use == "None":
            try:
                os.remove("pos_ang.p")
                os.remove("road.p")
                os.remove("reward.p")
            except:
                pass

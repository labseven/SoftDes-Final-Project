import sys
from main_ml_wrapper import GameState
from view import View
import random
import numpy as np

import argparse
from collections import deque

# from keras import initializations
# from keras.initializations import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.recurrent import LSTM
from keras.optimizers import SGD , Adam
import tensorflow as tf

ACTIONS = 4 # Number of ACTIONS
GAMMA = .99
OBSERVATION = 3200. # timesteps to observe before training
EXPLORE = 3000000. # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001 # final value of epsilon
INITIAL_EPSILON = 0.1 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # size of minibatch
FRAME_PER_ACTION = 1
LEARNING_RATE = 1e-4
NUMBEROFLIDAR = 30


def buildModel():
    print("Building the model...")
    model = Sequential()

    # Some crap. Learn the ml things
    model.add(LSTM(32, input_shape=(4,NUMBEROFLIDAR)))
    # model.add(Flatten())
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(ACTIONS))
    # model.add(Activation('hard_sigmoid'))
    model.add(Activation('softplus'))

    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss='mse',optimizer=adam)
    print("Done building the model.")
    return model

def trainNetwork(model, args):

    game = GameState()
    view = View(map_in = game.world)
    D = deque()

    if args['mode'] == 'Run':
        OBSERVE = 999999999    #We keep observe, never train
        epsilon = FINAL_EPSILON
        print ("Importing weights")
        model.load_weights("model.h5")
        adam = Adam(lr=LEARNING_RATE)
        model.compile(loss='mse',optimizer=adam)
        print ("Weights load successfully")
    else:                       #We go to training mode
        OBSERVE = OBSERVATION
        epsilon = INITIAL_EPSILON

    t = 0

    frame_actions = [0]*ACTIONS
    lidar_data, reward, terminal = game.next_frame(frame_actions)
    stack_t = np.stack((lidar_data, lidar_data, lidar_data, lidar_data), axis=0)
    # print(stack_t)
    # print(stack_t[:, :3])
    stack_t = stack_t.reshape(1, stack_t.shape[0], stack_t.shape[1])
    # print(stack_t)

    while True:
        """ Runs the simulation.
        """
        # Zero out variables
        loss = 0
        Q_sa = 0
        action_index = 0
        reward = 0
        frame_actions = np.zeros([ACTIONS])

        if t % FRAME_PER_ACTION == 0:
            if random.random() <= epsilon:
                print("----------Random Action----------")
                frame_actions = [random.getrandbits(1) for i in range(4)]
                # action_index = random.randrange(ACTIONS)
                # frame_actions[action_index] = 1
                print(frame_actions)
            else:
                print("NN prediction")
                q = model.predict(stack_t)       #input a stack of 4 lidar, get the prediction
                print(q)
                # max_Q = np.argmax(q)
                # action_index = max_Q
                # print(action_index)
                # frame_actions[max_Q] = 1
                frame_actions = q[0]

        lidar_data, reward, terminal = game.next_frame(frame_actions)
        lidar_data = np.asarray([[lidar_data]])
        stack_t1 = np.append(lidar_data, stack_t[:, :3], axis=1)
        # print(stack_t)

        D.append((stack_t, frame_actions, reward, stack_t1, terminal))
        if len(D) > REPLAY_MEMORY:
            D.popleft()

        view.draw_scene(game.world, [])

        stack_t = stack_t1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ML driver for corn racing')
    parser.add_argument('-m','--mode', help='Train / Run', required=True)
    args = vars(parser.parse_args())

    model = buildModel()
    trainNetwork(model, args)

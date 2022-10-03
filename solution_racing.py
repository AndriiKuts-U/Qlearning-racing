# your solution goes here, import whatever you need
import numpy as np
from collections import defaultdict
import dill
from racing import *
import matplotlib.pyplot as plt

class StudentAgent:
    def __init__(self, track, code=1, learning_rate=0.2, discount_factor=0.8, epsilon=0.2, env_iterations=400, test=False):
        self.random_rate = None
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.init_qtable()
        self.env_iterations = env_iterations
        self.actions, self.q_table = self.init_qtable()
        self.test_flag = test
        self.player_code = code
        self.states = []
        self.track = track
        self.road = []


    def get_code(self):
        return self.player_code

    def save_policy(self, filename):
        fw = open(filename, 'wb')
        dill.dump(self.q_table, fw)
        fw.close()

    def load_policy(self, filename):
        fr = open(filename, 'rb')
        self.q_table = dill.load(fr)
        fr.close()

    def init_qtable(self):
        actions = [x for x in range(4)]
        q_table = defaultdict(lambda: np.full(len(self.actions), 0.0))
        return actions, q_table

    def get_epsilon(self):
        return self.epsilon

    def act(self, state):
        state = tuple(state[2:4])
        free_pos = self.track.get_valid_actions_student(state)
        row = self.q_table[state]
        row = [row[i] for i in free_pos]
        max_q = np.max(row)

        if state not in self.states and not self.test_flag:
            self.states.append(state)
        if np.random.random() < self.get_epsilon():
            return np.random.choice(free_pos)
        if sum(row) == 0.0:
            return np.random.choice(free_pos)
        indeces = np.where(row == max_q)[0]
        if len(indeces) > 1:
            act = free_pos[np.random.choice(indeces)]
            return act
        else:
            return free_pos[indeces[0]]

    def compute_new_q_value(self, old_val, reward, next_value):
        return old_val + self.learning_rate * (reward + self.discount_factor * next_value - old_val)

    def learn(self, action, reward, done):
        for st in reversed(self.states):
            self.q_table[st][action] += self.learning_rate * (self.discount_factor * reward - self.q_table[st][action])
            reward = self.q_table[st][action]
        if done:
            self.states = []


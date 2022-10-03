import numpy as np


class Racing:
    def __init__(self):
        self.reset()

    def reset(self):
        self.track = np.full((10, 24), '.', dtype='str')
        self.track[0] = 'W'

        self.track[1, 0:3] = 'W'
        self.track[1, 12] = 'W'
        self.track[1, -1] = 'W'
        self.track[1, 8] = 'S'
        self.track[1, 13:15] = 'S'
        self.track[1, -2] = 'S'

        self.track[2, 0:2] = 'W'
        self.track[2, 4:7] = 'W'
        self.track[2, 12] = 'W'
        self.track[2, -1] = 'W'
        self.track[2, 13] = 'S'
        self.track[2, 18:21] = 'S'

        self.track[3, 0] = 'W'
        self.track[3, 8:10] = 'W'
        self.track[3, 16:21] = 'W'
        self.track[3, -1] = 'W'
        self.track[3, 5] = 'S'
        self.track[3, -2] = 'S'
        self.track[3, 11] = 'O'

        self.track[4, 3:6] = 'W'
        self.track[4, 14] = 'W'
        self.track[4, 20] = 'W'
        self.track[4, 8] = 'S'
        self.track[4, 13] = 'O'
        self.track[4, -1] = 'G'

        self.track[-5, 3:6] = 'W'
        self.track[-5, 14] = 'W'
        self.track[-5, 20] = 'W'
        self.track[-5, 8] = 'S'
        self.track[-5, 13] = 'O'
        self.track[-5, -1] = 'G'

        self.track[-4, 0] = 'W'
        self.track[-4, 8:10] = 'W'
        self.track[-4, 16:21] = 'W'
        self.track[-4, -1] = 'W'
        self.track[-4, 5] = 'S'
        self.track[-4, -2] = 'S'
        self.track[-4, 11] = 'O'

        self.track[-3, 0:2] = 'W'
        self.track[-3, 4:7] = 'W'
        self.track[-3, 12] = 'W'
        self.track[-3, -1] = 'W'
        self.track[-3, 13] = 'S'
        self.track[-3, 18:21] = 'S'

        self.track[-2, 0:3] = 'W'
        self.track[-2, 12] = 'W'
        self.track[-2, -1] = 'W'
        self.track[-2, 8] = 'S'
        self.track[-2, 13:15] = 'S'
        self.track[-2, -2] = 'S'

        self.track[-1] = 'W'

        self.p1_pos = (4, 0)
        self.p1_active = True

        self.p2_pos = (5, 0)
        self.p2_active = True
        return self.get_state()

    def has_won(self):
        # returns the code of the player who has won (1 or -1)
        # returns 3 if both cars are in the goal
        # returns 0 if the game hasn't yet been won
        p1_win = self.track[self.p1_pos] == 'G'
        p2_win = self.track[self.p2_pos] == 'G'

        if p1_win and p2_win:
            return 3

        if p1_win:
            return 1

        if p2_win:
            return -1

        return 0

    def is_done(self):
        # checks if the game is over:
        # it has been won or both cars have crashed

        # if someone won, end of game
        if self.has_won() != 0:
            return True

        # if (self.p1_active is False and self.p2_active is False):
        #     print(not self.p1_active and not self.p2_active, self.p1_pos, self.p2_pos)
        #     for i in range(10):
        #         print(list(self.track[i]))
        #     print("\n")
        # otherwise check if both cars have crashed
        return not self.p1_active and not self.p2_active

    def get_state(self):
        # returns the state:
        # position of player1 and player2 as a single np array
        p1_y, p1_x = self.p1_pos
        p2_y, p2_x = self.p2_pos
        return np.array([p1_y, p1_x, p2_y, p2_x])

    def get_reward(self):
        # 1 if player 1 wins
        # -1 if player 2 wins (player 1 loses)
        # 0 for draw or otherwise
        result = self.has_won()

        if result == -1:
            return -1
        elif result == 1:
            return 1
        else:
            return 0

    def get_reward_for_student(self):
        # 1 if player 1 wins
        # -1 if player 2 wins (player 1 loses)
        # 0 for draw or otherwise
        result = self.has_won()
        if self.p2_pos == self.p1_pos:
            return -2
        if result == -1:
            return 2
        elif result == 1:
            return -2
        else:
            if result == 3:
                return 0
            if self.track[self.p2_pos] == 'S':
                return -2
            if self.track[self.p2_pos] == 'O':
                return -2
            # if(self.p2_pos[1] >= 5):
            #     print(self.p2_pos, -1 + 1/(12 - self.p2_pos[1]), 1/(24 - self.p2_pos[1]))
            if self.p2_pos[1] < 12:
                return -1 + 1/(12 - self.p2_pos[1])
            else:
                return 1/(24 - self.p2_pos[1])



    def get_next_pos(self, pos, action):
        # N - 0, E - 1, S - 2, W - 3
        agent_y, agent_x = pos
        if action == 0:
            agent_y = max(0, agent_y - 1)
        elif action == 1:
            agent_x = min(23, agent_x + 1)
        elif action == 2:
            agent_y = min(agent_y + 1, 9)
        elif action == 3:
            agent_x = max(0, agent_x - 1)
        else:
            raise ValueError("Unknown action", action)

        next_pos = (agent_y, agent_x)
        if self.track[next_pos] == 'W':
            return pos, False

        return next_pos, True

    def slip_on_oil(self, pos):
        action = np.random.randint(0, 4)

        next_pos, active = self.get_next_pos(pos, action)
        # check for crash
        if active:
            return self.get_next_pos(next_pos, action)

        return next_pos, active

    def move_player(self, pos, action):
        # if the agent generates an invalid action, choose randomly
        if action not in [0, 1, 2, 3]:
            action = np.random.randint(0, 4)

        # only move in sand with 20% probability
        if self.track[pos] == 'S':
            if np.random.random() > 0.2:
                return pos, True

        # move in oil differently
        if self.track[pos] == 'O':
            return self.slip_on_oil(pos)

        # check for crash against wall
        return self.get_next_pos(pos, action)

    def step(self, p1_action, p2_action):
        orig_state = self.get_state()

        n_p1_pos = self.p1_pos
        n_p2_pos = self.p2_pos
        n_p1_active = False
        n_p2_active = False

        # takes player actions, and enacts them
        if self.p1_active:
            n_p1_pos, n_p1_active = self.move_player(self.p1_pos, p1_action)
        if self.p2_active:
            n_p2_pos, n_p2_active = self.move_player(self.p2_pos, p2_action)

        # print(n_p2_pos, n_p2_active)
        # if(self.p2_active == False or self.p1_active == False or n_p1_active == False or n_p2_active == False):
        #     print(self.p1_active, self.p2_active, self.p1_pos, self.p2_pos, p2_action)
        # check for cars crashing into each other
        if n_p1_pos == n_p2_pos:
            self.p1_pos = n_p1_pos
            self.p1_active = False

            self.p2_pos = n_p2_pos
            self.p2_active = False
            # print(orig_state, p1_action, p2_action)
        elif n_p1_pos == self.p2_pos and n_p2_pos == self.p1_pos:
            # print(self.p1_active, self.p2_active, self.p1_pos, self.p2_pos, p2_action)
            self.p1_active = False
            self.p2_active = False
        else:
            # no crash, update accordingly
            self.p1_pos = n_p1_pos
            self.p1_active = n_p1_active

            self.p2_pos = n_p2_pos
            self.p2_active = n_p2_active

        reward = self.get_reward()
        normal_reward = self.get_reward_for_student()
        done = self.is_done()
        state_copy = self.track.copy()
        state_copy[self.p1_pos] = 1
        state_copy[self.p2_pos] = 2
        info = {
            "state1": orig_state,
            "p1_action": p1_action,
            "p2_action": p2_action,
            "state2": self.get_state(),
            "reward": reward,
            "normal_reward": normal_reward,
            "done": done,
            "map": state_copy
        }

        return self.get_state(), reward, done, info

    def get_avoid_wall_actions(self, pos):
        # returns a list of actions not resulting in crash against wall
        actions = list()
        for action in range(4):
            next_pos, active = self.get_next_pos(pos, action)

            if active:
                actions.append(action)

        return actions

    def get_valid_actions(self, pos):
        # returns a list of actions leading to empty positions
        actions = list()
        for action in range(4):
            next_pos, active = self.get_next_pos(pos, action)

            if active and self.track[next_pos] != 'W' and next_pos != pos and next_pos != self.p2_pos:
                actions.append(action)

        return actions

    def get_next_pos_student(self, pos, action):
        # N - 0, E - 1, S - 2, W - 3
        agent_y, agent_x = pos
        if action == 0:
            agent_y = max(0, agent_y - 1)
        elif action == 1:
            agent_x = min(23, agent_x + 1)
        elif action == 2:
            agent_y = min(agent_y + 1, 9)
        elif action == 3:
            agent_x = max(0, agent_x - 1)
        else:
            raise ValueError("Unknown action", action)

        next_pos = (agent_y, agent_x)
        if self.track[next_pos] == 'W':
            return pos, False

        return next_pos, True

    def get_valid_actions_student(self, pos):
        # returns a list of actions leading to empty positions
        actions = list()
        for action in range(4):
            next_pos, active = self.get_next_pos_student(pos, action)

            if active and self.track[next_pos] != 'W' and next_pos != pos and next_pos != self.p1_pos:
                actions.append(action)
        # print(pos, actions)
        return actions


if __name__ == '__main__':
    test = Racing()

    for x in range(0, 24):
        for y in range(0, 10):
            if test.track[y, x] == 'S':
                for action in [0, 1, 2, 3]:
                    new_pos, active = test.move_player((y, x), action)
                    print((y, x), action, new_pos, active)
                print()

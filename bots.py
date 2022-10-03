import random

from racing import Racing

HELPER = Racing()


class RandomBot:
    def __init__(self, code=1):
        self.code = code

    def get_code(self):
        return self.code

    def act(self, state):
        return random.randint(0, 3)

class StupidBot:
    def __init__(self, code=1):
        self.code = code

    def get_code(self):
        return self.code

    def act(self, state):
        return 0

class SmartBot:
    def __init__(self, code=1):
        self.code = code

    def get_code(self):
        return self.code

    def act(self, state):
        if self.code == 1:
            pos = (state[0], state[1])
        else:
            pos = (state[2], state[3])

        actions = HELPER.get_avoid_wall_actions(pos)
        return random.choice(actions)


class SmarterBot:
    def __init__(self, code=1):
        self.code = code

    def get_code(self):
        return self.code

    def act(self, state):
        if self.code == 1:
            pos = (state[0], state[1])
        else:
            pos = (state[2], state[3])

        actions = HELPER.get_valid_actions(pos)
        return random.choice(actions)

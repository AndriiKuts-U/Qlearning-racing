import random

from bots import RandomBot, SmartBot, SmarterBot, StupidBot
from solution_racing import StudentAgent
from racing import Racing
import random
import time
if __name__ == '__main__':
    test = True
    track = Racing()
    agents = [RandomBot(code=1), SmartBot(code=1), SmarterBot(code=1)]
    player_1 = RandomBot(code=1)
    player_2 = StudentAgent(track, code=-1, test=test)

    one_wins = 0
    two_wins = 0
    both_wins = 0
    dnfs = 0
    TESTS = 100000
    if test is True:
        player_2.load_policy("agent_racer")
        print(player_2.q_table)
    for ts in range(TESTS):
        track.reset()

        while not track.is_done():
            state = track.get_state().copy()

            # get player moves
            p1_move = player_1.act(state)
            p2_move = player_2.act(state)
            # print(p2_move)
            new_state, reward, done, info = track.step(p1_move, p2_move)
            if not test:
                player_2.learn(p2_move, info["normal_reward"], done)

        result = track.has_won()
        if result == 3:
            both_wins += 1
        if result == 1:
            one_wins += 1
        elif result == -1:
            two_wins += 1
        else:
            dnfs += 1

        if ts % 1000 == 0 and ts != 0:
            for i in range(10):
                print(list(info["map"][i]))
            print("\n")
            print("{} epoch: {} player 1 wins ({:.2f}%); {} player 2 wins ({:.2f}%); {} ties ({:.2f}%); {} DNFs ({:.2f}%)".format(
                        ts/1000,
                        one_wins, 100 * one_wins / 1000,
                        two_wins, 100 * two_wins / 1000,
                        both_wins, 100 * both_wins / 1000,
                        dnfs, 100 * dnfs / 1000))
            if test is False:
                player_2.save_policy("agent_racer")
            one_wins = 0
            two_wins = 0
            both_wins = 0
            dnfs = 0

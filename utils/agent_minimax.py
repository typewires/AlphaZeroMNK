from random import choice
from utils.search_core import copy_env, candidate_moves


def MiniMax_depth_mnk(env, depth=3, radius=1):
    wins, ties, losses = [], [], []
    for m in candidate_moves(env, radius):
        env_copy = copy_env(env)
        state, reward, done, info = env_copy.step(m)
        if done and reward != 0:           # immediate win for the mover
            return m
        opponent_payoff = max_payoff_mnk(env_copy, reward, done,
                                         depth, radius)
        my_payoff = -opponent_payoff
        if my_payoff == 1:
            wins.append(m)
        elif my_payoff == 0:
            ties.append(m)
        else:
            losses.append(m)
    if wins:
        return choice(wins)
    elif ties:
        return choice(ties)
    if losses:
        return choice(losses)
    return env.sample()


def max_payoff_mnk(env, reward, done, depth, radius=1):
    # if the game has ended after the previous player's move
    if done:
        return -1 if reward != 0 else 0
    # If the maximum depth is reached, assume tie game
    # (later replace this 0 with rollouts / a value network)
    if depth == 0:
        return 0
    best_payoff = -2
    for m in candidate_moves(env, radius):
        env_copy = copy_env(env)
        state, reward, done, info = env_copy.step(m)
        opponent_payoff = max_payoff_mnk(env_copy, reward, done,
                                         depth - 1, radius)
        my_payoff = -opponent_payoff
        if my_payoff > best_payoff:
            best_payoff = my_payoff
    return best_payoff

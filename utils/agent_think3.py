import random
from utils.search_core import copy_env


def _win_in_1(env, want):
    for m in env.validinputs:
        ec = copy_env(env)
        state, reward, done, info = ec.step(m)
        if done and reward == want:
            return m
    return None


def _lose_in_2(env, opp_want):
    for m1 in env.validinputs:
        for m2 in env.validinputs:
            if m1 != m2:
                ec = copy_env(env)
                ec.step(m1)
                state, reward, done, info = ec.step(m2)
                if done and reward == opp_want:
                    return m2
    return None


def think3_fast(env):
    want = 1 if env.turn == "X" else -1
    opp_want = -want
    if len(env.validinputs) == 1:
        return env.validinputs[0]
    w = _win_in_1(env, want)
    if w is not None:
        return w
    l = _lose_in_2(env, opp_want)
    if l is not None:
        return l
    if len(env.validinputs) <= 2:
        return random.choice(env.validinputs)
    w3 = []
    vi = env.validinputs
    for m1 in vi:
        for m2 in vi:
            for m3 in vi:
                if m1 != m2 and m1 != m3 and m2 != m3:
                    ec = copy_env(env)
                    ec.step(m1); ec.step(m2)
                    state, reward, done, info = ec.step(m3)
                    if done and reward == want:
                        w3.append(m1)
    if len(w3) > 0:
        return max(set(w3), key=w3.count)
    return random.choice(vi)

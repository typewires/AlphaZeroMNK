from copy import deepcopy
from utils.mnk_simple_env import mnk


def copy_env(env):
    if type(env) is not mnk:
        return deepcopy(env)
    c = mnk.__new__(mnk)                  
    c.cols, c.rows, c.k = env.cols, env.rows, env.k
    c.ncells = env.ncells
    c.action_space = env.action_space    
    c.observation_space = env.observation_space
    c.info = env.info
    c.turn = env.turn
    c.validinputs = list(env.validinputs)
    c.state = env.state.copy()
    c.done = env.done
    c.reward = env.reward
    c.last_move = env.last_move
    c.winning_cells = list(env.winning_cells)
    return c


def candidate_moves(env, radius=1):
    occupied = [(c, r) for c in range(env.cols)
                for r in range(env.rows) if env.state[c][r] != 0]
    if not occupied:                       
        cc, cr = (env.cols - 1) // 2, (env.rows - 1) // 2
        return [env.cell_to_move(cc, cr)]
    cands = []
    for m in env.validinputs:
        col, row = env.move_to_cell(m)
        if any(max(abs(col - c), abs(row - r)) <= radius
               for c, r in occupied):
            cands.append(m)
    return cands if cands else list(env.validinputs)

import os, time
from multiprocessing import Pool

from utils.mnk_simple_env import mnk
from utils.agent_minimax import MiniMax_depth_mnk
from utils.agent_think3 import think3_fast

RADIUS = 1  

def play_game_number(i):
  #  Returns +1 if MiniMax won, -1 if it lost, 0 tie 
    env = mnk(cols=6, rows=6, k=4)
    env.reset()
    minimax_is_X = (i % 2 == 0)
    while not env.done:
        if (env.turn == "X") == minimax_is_X:
            move = MiniMax_depth_mnk(env, depth=3, radius=RADIUS)
        else:
            move = think3_fast(env)
        env.step(move)
    flip = 1 if minimax_is_X else -1    
    return flip * env.reward


def run_match(games, processes=None):
    print(f"CPU cores available: {os.cpu_count()}")
    print(f"running {games} games...")
    start = time.time()
    with Pool(processes=processes) as pool:
        results = pool.map(play_game_number, range(games))
    elapsed = time.time() - start
    w, l, t = results.count(1), results.count(-1), results.count(0)
    print(f"\nfinished {games} games in {elapsed:.1f} s "
          f"({elapsed/games:.2f} s/game wall-clock)")
    print(f"MiniMax wins {w} | losses {l} | ties {t}")
    return results

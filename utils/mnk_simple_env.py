from random import choice
import numpy as np

class action_space:
    def __init__(self, n):
        self.n = n


class observation_space:
    def __init__(self, row, col):
        self.shape = (row, col)


class mnk():
    def __init__(self, cols=6, rows=6, k=4):
        self.cols = cols
        self.rows = rows
        self.k = k
        self.ncells = cols * rows
        self.action_space = action_space(self.ncells)
        self.observation_space = observation_space(cols, rows)
        self.info = ""
        self.reset()

    def move_to_cell(self, move):
        idx = move - 1
        row = idx // self.cols
        col = idx % self.cols
        return col, row

    def cell_to_move(self, col, row):
        return row * self.cols + col + 1

    def sample(self):
        return choice(self.validinputs)

    def reset(self):
        self.turn = "X"
        self.validinputs = list(range(1, self.ncells + 1))
        self.state = np.zeros((self.cols, self.rows), dtype=int)
        self.done = False
        self.reward = 0
        self.last_move = None
        self.winning_cells = []        
        return self.state

    def step(self, inp):
        col, row = self.move_to_cell(inp)
        mark = 1 if self.turn == "X" else -1

        self.state[col][row] = mark
        self.last_move = (col, row, self.turn)

        if inp in self.validinputs:
            self.validinputs.remove(inp)
        if self.win_game(col, row):
            self.done = True
            self.reward = 2 * (self.turn == "X") - 1   # +1 X, -1 O
            self.validinputs = []
        elif len(self.validinputs) == 0:
            self.done = True
            self.reward = 0
        else:
            self.turn = "O" if self.turn == "X" else "X"
        return self.state, self.reward, self.done, self.info

    def _count_dir(self, col, row, dcol, drow, mark):
        cells = []
        c, r = col + dcol, row + drow
        while 0 <= c < self.cols and 0 <= r < self.rows and self.state[c][r] == mark:
            cells.append((c, r))
            c += dcol
            r += drow
        return cells

    def win_game(self, col, row):
        mark = self.state[col][row]
        if mark == 0:
            return False

        for dcol, drow in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            forward = self._count_dir(col, row, dcol, drow, mark)
            backward = self._count_dir(col, row, -dcol, -drow, mark)
            line = backward[::-1] + [(col, row)] + forward
            if len(line) >= self.k:
                played_idx = len(backward)
                start = max(0, played_idx - (self.k - 1))
                for s in range(start, played_idx + 1):
                    if s + self.k <= len(line):
                        self.winning_cells = line[s:s + self.k]
                        return True
        return False

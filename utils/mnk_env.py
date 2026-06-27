import turtle as t
import time
from utils.mnk_simple_env import mnk


class mnk_gui(mnk):
    BOARD_BG    = "#C8A86B"   # warm tan board
    BOARD_EDGE  = "#B6925A"   # slightly darker outer frame
    INNER_LINE  = "#A9824B"   # thin inner border line
    LINE_COLOR  = "#3A2A12"   # grid lines / text
    SHADOW      = "#0e1a1f"   # drop shadow under the board
    TITLE_COLOR = "#F4E4B8"   # cream title text
    GOLD        = "#F2D75A"   # winner highlight ring

    def __init__(self, cols=6, rows=6, k=4):
        self.xs = [-300, -200, -100, 0, 100, 200, 300][:cols]
        self.ys = [-250, -150, -50, 50, 150, 250][:rows]
        if cols != 7 or rows != 6:
            cell = 100
            hw = (cols - 1) * cell / 2
            hh = (rows - 1) * cell / 2
            self.xs = [-hw + c * cell for c in range(cols)]
            self.ys = [-hh + r * cell for r in range(rows)]
        self.showboard = False
        self.status_pen = None
        super().__init__(cols=cols, rows=rows, k=k)


    def __deepcopy__(self, memo):
        import numpy as np
        clone = mnk(cols=self.cols, rows=self.rows, k=self.k)
        clone.turn = self.turn
        clone.validinputs = list(self.validinputs)
        clone.state = np.array(self.state, copy=True)
        clone.done = self.done
        clone.reward = self.reward
        clone.last_move = self.last_move
        clone.winning_cells = list(self.winning_cells)
        clone.info = self.info
        return clone

    def _draw_stone(self, px, py, colour, ghost=False, pen=None):
        p = pen if pen is not None else t
        p.up()
        if ghost:
            p.goto(px, py)
            p.dot(82, "#D8C27E" if colour == "black" else "#EFE7C8")
            p.dot(70, self.BOARD_BG)
            p.up()
            return
        if colour == "black":
            p.goto(px, py)
            p.dot(84, "#0c0c0c")       # rim
            p.dot(78, "#1b1b1b")       # body
            p.dot(60, "#262626")       # subtle inner sheen
            p.goto(px - 15, py + 15)
            p.dot(16, "#4a4a4a")       # highlight
        else:
            p.goto(px, py)
            p.dot(84, "#8a8a8a")       # rim
            p.dot(78, "#fafafa")       # body
            p.dot(60, "#ffffff")       # inner
            p.goto(px - 13, py + 13)
            p.dot(14, "#d8d8d8")       # soft highlight
        p.up()


    def display_board(self):
        try:
            t.setup(900, 760, 10, 40)
        except Exception:
            pass
        t.bgcolor("#1d2b33")          # dark space-blue backdrop
        t.hideturtle()
        t.tracer(False)
        t.title(f"{self.k} in a Row")

        # create all pens ONCE
        self.bg_pen = t.Turtle(); self.bg_pen.hideturtle(); self.bg_pen.up()
        self.label_pen = t.Turtle(); self.label_pen.hideturtle(); self.label_pen.up()
        self.status_pen = t.Turtle(); self.status_pen.hideturtle(); self.status_pen.up()
        self.stone_pen = t.Turtle(); self.stone_pen.hideturtle(); self.stone_pen.up()
        self.ghost_pen = t.Turtle(); self.ghost_pen.hideturtle(); self.ghost_pen.up()

        self._paint_static_board()
        self._update_status()

    def _paint_static_board(self):
        bg = self.bg_pen
        bg.clear()
        self.label_pen.clear()

        L = self.xs[0]; R = self.xs[-1]
        B = self.ys[0]; T = self.ys[-1]
        pad = 55
        bg.up(); bg.pensize(1)

        def rect(x0, y0, x1, y1, pencol, fillcol=None):
            bg.up(); bg.goto(x0, y0); bg.down()
            bg.color(pencol, fillcol if fillcol else pencol)
            if fillcol: bg.begin_fill()
            for (xx, yy) in [(x1, y0), (x1, y1), (x0, y1), (x0, y0)]:
                bg.goto(xx, yy)
            if fillcol: bg.end_fill()
            bg.up()

        rect(L - pad + 10, B - pad - 10, R + pad + 14, T + pad - 14,
             self.SHADOW, self.SHADOW)
        bg.pensize(2)
        rect(L - pad, B - pad, R + pad, T + pad, self.BOARD_EDGE, self.BOARD_EDGE)
        # inner board face
        rect(L - pad + 8, B - pad + 8, R + pad - 8, T + pad - 8,
             self.LINE_COLOR, self.BOARD_BG)
        # thin inner border line
        bg.pensize(1)
        rect(L - pad + 20, B - pad + 20, R + pad - 20, T + pad - 20, self.INNER_LINE)

        bg.color(self.LINE_COLOR); bg.pensize(1.5)
        for x in self.xs:
            bg.up(); bg.goto(x, B); bg.down(); bg.goto(x, T)
        for y in self.ys:
            bg.up(); bg.goto(L, y); bg.down(); bg.goto(R, y)
        bg.up()

        if self.cols == 7 and self.rows == 6:
            for (ci, ri) in [(1, 1), (1, 4), (3, 2), (5, 1), (5, 4)]:
                bg.goto(self.xs[ci], self.ys[ri]); bg.dot(11, self.LINE_COLOR)
        elif self.cols == 6 and self.rows == 6:
            for (ci, ri) in [(1, 1), (1, 4), (4, 1), (4, 4)]:
                bg.goto(self.xs[ci], self.ys[ri]); bg.dot(11, self.LINE_COLOR)

        lp = self.label_pen
        lp.color(self.LINE_COLOR); lp.up()
        # columns 1..cols along the top
        for i, x in enumerate(self.xs):
            lp.up(); lp.goto(x, T + pad - 38)
            lp.write(i + 1, align="center", font=("Arial", 16, "bold"))
            
        for i, y in enumerate(self.ys):
            lp.up(); lp.goto(L - pad - 28, y - 10)
            lp.write(i + 1, align="center", font=("Arial", 16, "bold"))
            lp.up(); lp.goto(R + pad + 28, y - 10)
            lp.write(i + 1, align="center", font=("Arial", 16, "bold"))

        # title
        bg.color(self.TITLE_COLOR)
        bg.up(); bg.goto(0, T + pad + 45)
        bg.write(f"{self.k} in a Row", align="center", font=("Arial", 30, "bold"))
        # bottom caption
        bg.goto(0, B - pad - 30)
        bg.write("click any empty intersection to place a stone   |   press r to reset   |   q to quit",
                 align="center", font=("Arial", 14, "normal"))
        t.update()

    def _update_status(self):
        if self.status_pen is None:
            return
        if self.done:
            if self.reward == 0:
                msg = "Draw!"
            else:
                winner = "Black" if self.reward == 1 else "White"
                msg = f"{winner} wins!"
        else:
            who = "Black" if self.turn == "X" else "White"
            msg = f"{who}'s turn"
        self.status_pen.clear()
        self.status_pen.color(self.LINE_COLOR)
        self.status_pen.up()
        self.status_pen.goto(0, self.ys[0] - 30)
        self.status_pen.write(msg, align="center", font=("Arial", 15, "bold"))
        t.update()

    def _ensure_board(self):
        if not self.showboard:
            self.display_board()
            self.showboard = True

    def preview(self, move, pause=0.35):
        self._ensure_board()
        col, row = self.move_to_cell(move)
        colour = "black" if self.turn == "X" else "white"
        self.ghost_pen.clear()
        self._draw_stone(self.xs[col], self.ys[row], colour,
                         ghost=True, pen=self.ghost_pen)
        t.update()
        if pause:
            time.sleep(pause)

    def render(self):
        self._ensure_board()
        if hasattr(self, "ghost_pen"):
            self.ghost_pen.clear()
        if self.last_move is not None:
            col, row, mark = self.last_move
            colour = "black" if mark == "X" else "white"
            self._draw_stone(self.xs[col], self.ys[row], colour,
                             pen=self.stone_pen)
            t.update()
        if self.done and self.winning_cells:
            for (cx, cy) in self.winning_cells:
                # gold halo ring behind the winning stone
                self.stone_pen.up()
                self.stone_pen.goto(self.xs[cx], self.ys[cy])
                self.stone_pen.dot(96, self.GOLD)
                mark = self.state[cx][cy]
                self._draw_stone(self.xs[cx], self.ys[cy],
                                 "black" if mark == 1 else "white",
                                 pen=self.stone_pen)
            t.update()
        self._update_status()

    def close(self):
        time.sleep(1)
        # With `%gui tk` active in Jupyter, plain t.bye() closes cleanly.
        try:
            t.bye()
        except Exception as e:
            print(f"exit turtle: {e}")
        self.showboard = False


def _nearest_intersection(px, py, xs, ys, snap=45):
    best_d, best = snap + 1, None
    for ci, x in enumerate(xs):
        for ri, y in enumerate(ys):
            d = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
            if d < best_d:
                best_d, best = d, (ci, ri)
    return best


def play_mouse(env=None, ai_agent=None, human_color="X", ai_agent2=None):
    if env is None:
        env = mnk_gui(cols=6, rows=6, k=4)
    env.reset()
    env.render()

    ai_vs_ai = (ai_agent is not None and ai_agent2 is not None)

    def maybe_ai_move():
        if ai_vs_ai:
            while not env.done:
                agent = ai_agent if env.turn == "X" else ai_agent2
                mv = agent(env)
                env.preview(mv, pause=0.25)
                env.step(mv)
                env.render()
        else:
            while (ai_agent is not None and not env.done
                   and env.turn != human_color):
                mv = ai_agent(env)
                env.preview(mv, pause=0.25)
                env.step(mv)
                env.render()

    maybe_ai_move()

    def on_click(px, py):
        if env.done or ai_vs_ai:        
            return
        if ai_agent is not None and env.turn != human_color:
            return
        cell = _nearest_intersection(px, py, env.xs, env.ys)
        if cell is None:
            return
        move = env.cell_to_move(*cell)
        if move not in env.validinputs:
            return
        env.step(move)
        env.render()
        maybe_ai_move()

    def restart():
        for attr in ("stone_pen", "ghost_pen", "status_pen"):
            pen = getattr(env, attr, None)
            if pen is not None:
                try:
                    pen.clear()
                except Exception:
                    pass
        env.reset()
        env.last_move = None
        if getattr(env, "bg_pen", None) is not None:
            env._paint_static_board()   # fresh empty board
            env._update_status()
        else:
            env.showboard = False
            env.render()
        t.onscreenclick(on_click)
        t.onkeypress(restart, "r")
        t.listen()
        maybe_ai_move()

    def quit_game():
        try:
            t.bye()
        except Exception as e:
            print(f"exit turtle: {e}")

    t.onscreenclick(on_click)
    t.onkeypress(restart, "r")
    t.onkeypress(quit_game, "q")
    t.onkeypress(quit_game, "Escape")
    t.listen()
    try:
        t.Screen()._root.protocol("WM_DELETE_WINDOW", quit_game)
    except Exception:
        pass
    import sys as _sys
    in_ipython = "IPython" in _sys.modules
    gui_tk_active = False
    if in_ipython:
        try:
            ip = _sys.modules["IPython"].get_ipython()
            # active_eventloop is 'tk' when %gui tk has been run
            gui_tk_active = getattr(ip, "active_eventloop", None) == "tk"
        except Exception:
            gui_tk_active = False
    if not gui_tk_active:
        try:
            t.mainloop()
        except Exception:
            pass


if __name__ == "__main__":
    play_mouse()

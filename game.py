import numpy as np


class GameLogic:
    def __init__(self, board_size=12, colors=None):
        self.board_size = board_size
        self.colors = colors or ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
        self.board = np.random.choice(self.colors, (self.board_size, self.board_size))
        self.move_count = 0
        self.max_moves = 22
        self.best_score = 22
        self.move_in_progress = False

    def make_move(self, color):
        if self.move_in_progress:
            return

        self.move_in_progress = True
        self.move_count += 1
        self.fill(0, 0, self.board[0, 0], color)

        if (self.board == color).all():
            self.best_score = min(self.best_score, self.move_count)
            self.reset_board()
            return "win"
        elif self.move_count == self.max_moves:
            self.reset_board()
            return "lose"

        self.move_in_progress = False
        return None

    def fill(self, i, j, old_color, new_color):
        stack = [(i, j)]
        while stack:
            i, j = stack.pop()
            if i < 0 or j < 0 or i >= self.board_size or j >= self.board_size:
                continue
            if self.board[i, j] != old_color:
                continue
            self.board[i, j] = new_color
            stack.append((i - 1, j))
            stack.append((i + 1, j))
            stack.append((i, j - 1))
            stack.append((i, j + 1))

    def reset_board(self):
        self.board = np.random.choice(self.colors, (self.board_size, self.board_size))
        self.move_count = 0
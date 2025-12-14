import random
from time import sleep
from config import ANIMATION_DELAY


def solveNQueens(board, col, n, gui_callback=None):
    attempts = {"count": 0}
    cols_order = list(range(n))

    def helper(board, col):
        if col >= n:
            return True
        random.shuffle(cols_order)
        for row in cols_order:
            attempts["count"] += 1
            if all(board.positions[r] != row and abs(board.positions[r]-row) != abs(r-col)
                   for r in range(col) if board.positions[r] != -1):
                board.positions[col] = row
                if gui_callback:
                    gui_callback(board.positions)
                    sleep(ANIMATION_DELAY)
                if helper(board, col+1):
                    return True
                board.positions[col] = -1
        return False

    helper(board, col)
    return board.positions, attempts["count"]
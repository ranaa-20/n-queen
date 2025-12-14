import random

class Board:
    def __init__(self, n, positions=None):
        self.n = n
        self.positions = [-1]*n if positions is None else positions[:]

    def is_goal(self, heuristic_fn):
        return -1 not in self.positions and heuristic_fn(self.positions) == 0

    def next_empty_row(self):
        for i, v in enumerate(self.positions):
            if v == -1:
                return i
        return None

    def generate_children(self):
        row = self.next_empty_row()
        if row is None:
            return []
        children = []
        for col in range(self.n):
            if all(self.positions[r] != col and abs(self.positions[r]-col) != abs(r-row)
                   for r in range(row) if self.positions[r] != -1):
                new_board = Board(self.n, self.positions)
                new_board.positions[row] = col
                children.append(new_board)
        return children

    @staticmethod
    def heuristic1(state):
        h = 0
        n = len(state)
        for i in range(n):
            for j in range(i+1, n):
                if state[i] != -1 and state[j] != -1:
                    if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                        h += 1
        return h

    @staticmethod
    def heuristic2(state):
        conflicted = set()
        n = len(state)
        for i in range(n):
            for j in range(i+1, n):
                if state[i] != -1 and state[j] != -1:
                    if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                        conflicted.add(i)
                        conflicted.add(j)
        return len(conflicted)
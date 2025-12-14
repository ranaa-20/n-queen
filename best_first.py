import random, heapq, itertools
from time import sleep
from board import Board
from config import ANIMATION_DELAY


def BestFirstSearch_H1(n, gui_callback=None, max_restarts=100):
    total_steps = 0
    for _ in range(max_restarts):
        counter = itertools.count()
        init_pos = [-1]*n
        init_pos[0] = random.randint(0, n-1)
        initial = Board(n, init_pos)

        pq = []
        heapq.heappush(pq, (Board.heuristic1(initial.positions), next(counter), initial))

        while pq:
            _, _, board = heapq.heappop(pq)
            total_steps += 1
            if gui_callback:
                gui_callback(board.positions)
                sleep(ANIMATION_DELAY)
            if board.is_goal(Board.heuristic1):
                return board.positions, total_steps
            for child in board.generate_children():
                heapq.heappush(pq, (Board.heuristic1(child.positions), next(counter), child))
    return None, total_steps


def BestFirstSearch_H2(n, gui_callback=None, max_restarts=100):
    total_steps = 0
    for _ in range(max_restarts):
        counter = itertools.count()
        init_pos = [-1]*n
        init_pos[0] = random.randint(0, n-1)
        initial = Board(n, init_pos)

        pq = []
        heapq.heappush(pq, (Board.heuristic2(initial.positions), next(counter), initial))

        while pq:
            _, _, board = heapq.heappop(pq)
            total_steps += 1
            if gui_callback:
                gui_callback(board.positions)
                sleep(ANIMATION_DELAY)
            if board.is_goal(Board.heuristic2):
                return board.positions, total_steps
            for child in board.generate_children():
                heapq.heappush(pq, (Board.heuristic2(child.positions), next(counter), child))
    return None, total_steps
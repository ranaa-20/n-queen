import random
from time import sleep
from config import ANIMATION_DELAY


def hill_climbing_solver(N, gui_callback=None):
    steps = 0
    def count_conflicts(state):
        conflicts = 0
        for i in range(N):
            for j in range(i+1, N):
                if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                    conflicts += 1
        return conflicts

    def generate_neighbor(state):
        best_state = state[:]
        best_conflicts = count_conflicts(state)
        for col in range(N):
            original_row = state[col]
            for row in range(N):
                if row != original_row:
                    new_state = state[:]
                    new_state[col] = row
                    new_conflicts = count_conflicts(new_state)
                    if new_conflicts < best_conflicts:
                        best_conflicts = new_conflicts
                        best_state = new_state[:]
        return best_state, best_conflicts

    for _ in range(1000):
        state = [random.randint(0, N-1) for _ in range(N)]
        conflicts = count_conflicts(state)
        while True:
            steps += 1
            if gui_callback:
                gui_callback(state)
                sleep(ANIMATION_DELAY)
            new_state, new_conflicts = generate_neighbor(state)
            if new_conflicts >= conflicts:
                break
            state, conflicts = new_state, new_conflicts
        if conflicts == 0:
            return state, steps
    return None, steps
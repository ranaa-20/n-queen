from config import ANIMATION_DELAY
from time import sleep
import numpy as np



def cultural_algorithm_solver(n, gui_callback=None, pop_size=50, gens=1000):
    steps = 0
    history = []
    def init_population(pop_size, n):
        return np.array([np.random.permutation(n) for _ in range(pop_size)])
    def conflicts(ind):
        return sum(abs(ind[i]-ind[j])==abs(i-j) for i in range(n) for j in range(i+1,n))
    def fitness(pop):
        return np.array([-conflicts(ind) for ind in pop])
    def init_belief_space(n):
        return {"normative": np.array([[0,n-1] for _ in range(n)]), "situational": None}
    def acceptance(pop, fit, percent=0.2):
        k = max(1,int(len(pop)*percent))
        idx = np.argsort(fit)[-k:]
        return pop[idx]
    def update_belief(belief, accepted):
        best = min(accepted,key=conflicts)
        belief["situational"]=best.copy()
        for pos in range(len(best)):
            vals = accepted[:,pos]
            belief["normative"][pos,0]=vals.min()
            belief["normative"][pos,1]=vals.max()
    def influence(pop, belief,p_sit=0.5,p_norm=0.5):
        new_pop = pop.copy()
        for i in range(len(pop)):
            if belief["situational"] is not None and np.random.rand()<p_sit:
                pos = np.random.randint(n)
                new_pop[i][pos] = belief["situational"][pos]
            if np.random.rand()<p_norm:
                pos=np.random.randint(n)
                low,high=belief["normative"][pos]
                new_pop[i][pos]=np.random.randint(low,high+1)
            used = set()
            missing = [x for x in range(n) if x not in new_pop[i]]
            for j in range(n):
                if new_pop[i][j] in used:
                    new_pop[i][j]=missing.pop()
                else:
                    used.add(new_pop[i][j])
        return new_pop

    pop = init_population(pop_size,n)
    belief = init_belief_space(n)
    for g in range(gens):
        steps += 1
        fit = fitness(pop)
        best_idx = fit.argmax()
        history.append(-fit[best_idx])  # سجل أفضل قيمة لكل جيل
        if gui_callback:
            gui_callback(pop[best_idx])
            sleep(ANIMATION_DELAY)
        if fit[best_idx]==0:
            return pop[best_idx], steps, history
        accepted = acceptance(pop,fit)
        update_belief(belief,accepted)
        pop = influence(pop,belief)
    return pop[fit.argmax()], steps, history

import numpy as np

class InventoryOptimizer:
    def __init__(self, T, I_max, x_max, demand_probs, demand_vals, c, h, p):
        self.T = T
        self.I_max = I_max
        self.x_max = x_max
        self.demand_probs = demand_probs
        self.demand_vals = demand_vals
        self.c = c
        self.h = h
        self.p = p
        self.V = np.full((T+1, I_max+1), np.inf)
        self.policy = np.zeros((T, I_max+1), dtype=int)

    def solve(self):
        self.V[self.T] = 0
        for t in reversed(range(self.T)):
            for I in range(self.I_max + 1):
                best_cost = np.inf
                best_x = 0
                for x in range(min(self.x_max, self.I_max - I) + 1):
                    cost = 0
                    for d, prob in zip(self.demand_vals, self.demand_probs):
                        next_I = I + x - d
                        hold = self.h * max(next_I, 0)
                        short = self.p * max(-next_I, 0)
                        cost += prob * (self.c * x + hold + short + self.V[t+1][max(0, next_I)])
                    if cost < best_cost:
                        best_cost = cost
                        best_x = x
                self.V[t][I] = best_cost
                self.policy[t][I] = best_x
        return self.V, self.policy

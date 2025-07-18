#!/usr/bin/env python3
"""
Cálculo de Value at Risk (VaR) para el costo total de inventario (Sección 8.3.2)
Compute VaR at niveles α = 0.95 y 0.99 usando simulación Monte Carlo.
"""
import numpy as np
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

# Parámetros del problema (consistentes con Sección 8.3)
T = 12
I_max = 100
x_max = 50
c_ts = np.full(T, 10.0)  # costo de compra uniforme
h = 2.0                 # costo de almacenamiento
p = 20.0                # penalización por escasez

# Distribución base uniforme sobre {0..10}
support = np.arange(11)
probs = np.full(11, 1/11)

# Resolver DP para obtener política
dm = DemandModel(support.tolist(), probs.tolist())
solver = DynamicProgrammingSolver(T=T, I_max=I_max, x_max=x_max,
                                  costs={'c': c_ts, 'h': h, 'p': p},
                                  demand_dist=dm)
V, policy = solver.solve()

# Función para simular costo total dado la política
def simulate_cost(policy, support, probs, I_init=0, N=10000):
    costs = np.zeros(N)
    for i in range(N):
        I = I_init
        total = 0.0
        for t in range(T):
            x = int(policy[t, I])
            D = np.random.choice(support, p=probs)
            purchase = c_ts[t] * x
            hold = h * max(I + x - D, 0)
            short = p * max(D - I - x, 0)
            total += purchase + hold + short
            I = max(I + x - D, 0)
        costs[i] = total
    return costs

if __name__ == '__main__':
    # Simulación Monte Carlo
    N = 10000
    costs = simulate_cost(policy, support, probs, I_init=0, N=N)

    # Calcular VaR
    for alpha in [0.95, 0.99]:
        var = np.percentile(costs, alpha * 100)
        print(f"VaR (α={alpha}): {var:.1f}")

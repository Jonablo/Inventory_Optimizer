#!/usr/bin/env python3
"""
Comparación de métodos alternativos (Sección 7.3.3)
Métodos: Programación Dinámica, Heurística (s,S), Simulación Monte Carlo, Programación Lineal
"""
import time
import numpy as np
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel
from scipy.optimize import linprog

# Parámetros de prueba comunes
def run_comparison(T, I_max, x_max, support, probs, costs):
    # 1) Programación Dinámica
    dm = DemandModel(support, probs)
    dp_solver = DynamicProgrammingSolver(T=T, I_max=I_max, x_max=x_max,
                                         costs={'c': costs['c'], 'h': costs['h'], 'p': costs['p']},
                                         demand_dist=dm)
    t0 = time.perf_counter()
    V_dp, policy_dp = dp_solver.solve()
    t_dp = time.perf_counter() - t0
    cost_dp = float(V_dp[0, int(costs['initial_inventory'])])

    # 2) Heurística s,S basada en primer periodo
    orders = [(i, policy_dp[0, i]) for i in range(I_max + 1) if policy_dp[0, i] > 0]
    if orders:
        s, x = min(orders, key=lambda it: it[0])
        S = s + int(x)
    else:
        s = S = 0
    inv = costs['initial_inventory']
    cost_h = 0.0
    t0_h = time.perf_counter()
    for t in range(T):
        order = max(S - inv, 0) if inv < s else 0
        E_d = np.dot(support, probs)
        inv = max(inv + order - E_d, 0)
        cost_h += costs['c'][t] * order + costs['h'] * inv + costs['p'] * max(-inv, 0)
    t_h = time.perf_counter() - t0_h

    # 3) Simulación Monte Carlo
    N = 10000
    t0_mc = time.perf_counter()
    cost_mc = 0.0
    for _ in range(N):
        inv = costs['initial_inventory']
        for t in range(T):
            x = int(policy_dp[t, inv])
            d = np.random.choice(support, p=probs)
            inv = max(inv + x - d, 0)
            cost_mc += costs['c'][t] * x + costs['h'] * inv + costs['p'] * max(-inv, 0)
    cost_mc /= N
    t_mc = time.perf_counter() - t0_mc

    # 4) Programación Lineal
    # Variables: inv_1..inv_T, short_0..short_{T-1}, x_0..x_{T-1}
    n_inv = T
    n_short = T
    n_x = T
    n_vars = n_inv + n_short + n_x
    # Cost vector
    c = np.zeros(n_vars)
    c[:n_inv] = costs['h']
    c[n_inv:n_inv+n_short] = costs['p']
    c[n_inv+n_short:] = costs['c']

    # Build A_eq and b_eq
    A_eq = np.zeros((T+1, n_vars))
    b_eq = np.zeros(T+1)
    E_D = np.dot(support, probs)
    # t = 0
    A_eq[0, 0] = 1                # inv_1
    A_eq[0, n_inv+0] = 1         # short_0
    A_eq[0, n_inv+n_short+0] = -1 # x_0
    b_eq[0] = costs['initial_inventory'] - E_D
    # t = 1..T-1
    for t in range(1, T):
        A_eq[t, t] = 1            # inv_{t+1}
        A_eq[t, t-1] = -1         # inv_t
        A_eq[t, n_inv+t] = 1      # short_t
        A_eq[t, n_inv+n_short+t] = -1 # x_t
        b_eq[t] = -E_D
    # Terminal inv_T free, enforce inv_T >= 0 implicitly

    t0_lp = time.perf_counter()
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)]*n_vars, method='highs')
    t_lp = time.perf_counter() - t0_lp
    cost_lp = float(res.fun) if res.success else None

    return {
        'dp': (cost_dp, t_dp),
        'hs': (cost_h, t_h),
        'mc': (cost_mc, t_mc),
        'lp': (cost_lp, t_lp)
    }

if __name__ == '__main__':
    # Ejemplo según informe
    T = 12; I_max = 100; x_max = 50
    support = list(range(11)); probs = [1/11]*11
    costs = {'c': np.full(T, 10), 'h': 2, 'p': 20, 'initial_inventory': 10}
    results = run_comparison(T, I_max, x_max, support, probs, costs)
    for m, (cst, tme) in results.items():
        print(f"Método {m}: costo={cst}, tiempo={tme:.4f}s")

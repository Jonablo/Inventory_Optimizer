#!/usr/bin/env python3
"""
Experimentos Específicos (Sección 7.3.1)
Caso 1: Demanda constante
Caso 2: Demanda Poisson con penalización alta
Caso 3: Costos variables
"""
import numpy as np
import math
import time
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel


def run_case_constant_demand():
    T = 12
    I_init = 0  # Inicialmente sin inventario para verificar pedidos cada período
    I_max = 100
    x_max = 100
    # Costos según informe: c_t = 10, h = 2, p = 20
    costs = {'c': np.full(T, 10), 'h': 2, 'p': 20}
    # Demanda constante D_t = 5
    support = [5]
    probs = [1]

    dm = DemandModel(support, probs)
    solver = DynamicProgrammingSolver(
        T=T, I_max=I_max, x_max=x_max,
        costs=costs,
        demand_dist=dm
    )
    V, policy = solver.solve()

    # Simulación para calcular suma de órdenes desde I_init
    inventory = I_init
    total_order = 0
    for t in range(T):
        x = int(policy[t, inventory])
        total_order += x
        inventory = max(inventory + x - support[0], 0)

    total_cost = total_order * costs['c'][0]
    print("Caso 1: Demanda constante D=5 todo t, T=12, I0=0")
    print(f"  ∑ x_t = {total_order}, costo total = {total_cost}")

def run_case_poisson_high_penalty():
    T = 12
    I_init = 0
    I_max = 100
    x_max = 100
    # Demanda Poisson(3), p=100, h=1
    lam = 3
    max_d = 15
    support = list(range(max_d+1))
    # Usar math.exp y math.factorial en lugar de np.math
    raw = [math.exp(-lam) * lam**k / math.factorial(k) for k in support]
    total = sum(raw)
    probs = [p/total for p in raw]
    costs = {'c': np.full(T, 10), 'h': 1, 'p': 100}

    dm = DemandModel(support, probs)
    solver = DynamicProgrammingSolver(
        T=T, I_max=I_max, x_max=x_max,
        costs=costs,
        demand_dist=dm
    )
    start = time.perf_counter()
    V, policy = solver.solve()
    t_exec = time.perf_counter() - start

    print("Caso 2: Demanda Poisson(3), p=100, h=1")
    print(f"  Tiempo: {t_exec:.4f}s")
    # Extraer (s_t,S_t)
    summary = []
    for t in range(T):
        orders = [I for I, x in enumerate(policy[t]) if x > 0]
        if orders:
            s_t = min(orders)
            S_t = s_t + int(policy[t, s_t])
        else:
            s_t = None
            S_t = None
        summary.append((s_t, S_t))
    print("  (s_t, S_t) para t=0..T-1:", summary)


def run_case_variable_costs():
    T = 12
    I_init = 0
    I_max = 100
    x_max = 100
    # c_t = 10 + 5 sin(2πt/12)
    c_ts = 10 + 5 * np.sin(2 * np.pi * np.arange(T) / 12)
    costs = {'c': c_ts, 'h': 2, 'p': 20}
    support = list(range(11))
    probs = [1/11] * 11

    dm = DemandModel(support, probs)
    solver = DynamicProgrammingSolver(
        T=T, I_max=I_max, x_max=x_max,
        costs=costs,
        demand_dist=dm
    )
    V, policy = solver.solve()
    print("Caso 3: Costos variables c_t = 10+5 sin(2πt/12)")
    print("  Órdenes concentradas en periodos de bajo costo:")
    print(policy)


def main():
    run_case_constant_demand()
    print()
    run_case_poisson_high_penalty()
    print()
    run_case_variable_costs()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Análisis de Sensibilidad Paramétrica (Sección 8.1)
Varía los costos de almacenamiento y penalización y calcula V0 e incremento porcentual.
"""
import numpy as np
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

def solve_dp(T, I_max, x_max, c, h, p, support, probs, I0=0):
    """
    Resuelve DP y retorna V0 para inventario inicial I0.
    """
    costs = { 'c': np.full(T, c), 'h': h, 'p': p }
    dm = DemandModel(support, probs)
    solver = DynamicProgrammingSolver(
        T=T, I_max=I_max, x_max=x_max,
        costs=costs,
        demand_dist=dm
    )
    V, _ = solver.solve()
    return float(V[0, I0])

if __name__ == '__main__':
    # Parámetros base
    T = 12
    I_max = 100
    x_max = 50
    support = list(range(11))
    probs = [1/11] * 11
    I0 = 0
    c_base = 10
    h_base = 2
    p_base = 20

    # Sensibilidad a p
    print("Sensibilidad a la penalización p:")
    V_base = solve_dp(T, I_max, x_max, c_base, h_base, p_base, support, probs, I0)
    for p in [10, 20, 50]:
        V0 = solve_dp(T, I_max, x_max, c_base, h_base, p, support, probs, I0)
        delta = (V0 - V_base) / V_base * 100
        print(f"  p={p}: V0={V0:.1f}, Δ={delta:+.1f}%")

    # Sensibilidad a h
    print("\nSensibilidad al costo de almacenamiento h:")
    V_base = solve_dp(T, I_max, x_max, c_base, h_base, p_base, support, probs, I0)
    for h in [1, 2, 5]:
        V0 = solve_dp(T, I_max, x_max, c_base, h, p_base, support, probs, I0)
        delta = (V0 - V_base) / V_base * 100
        print(f"  h={h}: V0={V0:.1f}, Δ={delta:+.1f}%")

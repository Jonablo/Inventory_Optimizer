#!/usr/bin/env python3
"""
Análisis de Escenarios Determinísticos (Sección 8.3.1)
Escenarios:
  - Optimista: D_t = ⌊μ_D - σ_D⌉ (redondeado a entero)
  - Pesimista: D_t = ⌊μ_D + σ_D⌉ (redondeado a entero)
  - Realista: D_t sigue la distribución base
"""
import numpy as np
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

def solve_dp(T, I_max, x_max, c, h, p, support, probs):
    """
    Resuelve DP y retorna V0 (valor inicial) para distribución dada.
    """
    dm = DemandModel(support, probs)
    solver = DynamicProgrammingSolver(
        T=T, I_max=I_max, x_max=x_max,
        costs={'c': np.full(T, c), 'h': h, 'p': p},
        demand_dist=dm
    )
    V, _ = solver.solve()
    return float(V[0, 0])

if __name__ == '__main__':
    # Parámetros comunes
    T = 12
    I_max = 100
    x_max = 50
    c = 10
    h = 2
    p = 20

    # Distribución base uniforme sobre {0..10}
    support_base = list(range(11))
    probs_base = [1/11] * 11

    # Calcular μ y σ de la distribución base
    mu = np.dot(support_base, probs_base)
    sigma = np.sqrt(np.dot((np.array(support_base) - mu)**2, probs_base))

    # Escenario optimista: demanda constante redondeada
    d_opt_val = int(round(mu - sigma))
    d_opt_val = max(d_opt_val, 0)
    V_opt = solve_dp(T, I_max, x_max, c, h, p, [d_opt_val], [1.0])

    # Escenario pesimista: demanda constante redondeada
    d_pes_val = int(round(mu + sigma))
    d_pes_val = max(d_pes_val, 0)
    V_pes = solve_dp(T, I_max, x_max, c, h, p, [d_pes_val], [1.0])

    # Escenario realista (base)
    V_real = solve_dp(T, I_max, x_max, c, h, p, support_base, probs_base)

    # Mostrar resultados
    print(f"Escenario optimista: V0={V_opt:.1f}")
    print(f"Escenario pesimista: V0={V_pes:.1f}")
    print(f"Escenario realista: V0={V_real:.1f}")

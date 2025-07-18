#!/usr/bin/env python3
import time, math
import itertools
import numpy as np
import pandas as pd
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

def main():
    # Diseño experimental según informe
    T_vals = [6, 12, 24]
    I_vals = [50, 100, 200]
    x_vals = [20, 50, 100]
    D_support = np.arange(0, 11)               # |D| = 11
    D_probs   = np.full(11, 1/11)

    data = []
    for T, I_max, x_max in itertools.product(T_vals, I_vals, x_vals):
        # Modelo de demanda uniforme
        dm = DemandModel(D_support, D_probs)

        # Inicializar solver con costos según Escenario Estacionario (c_t=10,h=2,p=20)
        solver = DynamicProgrammingSolver(
            T=T,
            I_max=I_max,
            x_max=x_max,
            costs={'c': np.full(T, 10), 'h': 2, 'p': 20},
            demand_dist=dm
        )

        # Ejecutar y tomar tiempo de solución
        solver.solve()
        t_exec = solver.solution_time

        data.append({
            'T': T,
            'I_max': I_max,
            'x_max': x_max,
            'D_card': len(D_support),
            'T_exec': t_exec
        })
        print(f"  • T={T}, I_max={I_max}, x_max={x_max} → {t_exec:.4f}s")

    # DataFrame de resultados
    df = pd.DataFrame(data)

    # Variables log
    y = np.log(df['T_exec'].values)
    X_raw = np.column_stack([
        np.log(df['T'].values),
        np.log(df['I_max'].values),
        np.log(df['x_max'].values),
        np.log(df['D_card'].values),
    ])
    # Añadimos intercepto
    X = np.column_stack([np.ones(len(y)), X_raw])

    # Regresión por mínimos cuadrados
    β, *_ = np.linalg.lstsq(X, y, rcond=None)

    # Calcular R²
    y_pred = X.dot(β)
    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    R2 = 1 - ss_res/ss_tot

    # Mostrar resultados
    coef_names = ['α(intercept)', 'β₁(log T)', 'β₂(log I_max)', 'β₃(log x_max)', 'β₄(log |D|)']
    print("\nCoeficientes estimados (regresión log-log):")
    for name, val in zip(coef_names, β):
        print(f"  {name}: {val:.3f}")
    print(f"\nR² = {R2:.3f}")

    print("\nTabla de datos:", df.to_string(index=False))

if __name__ == "__main__":
    main()

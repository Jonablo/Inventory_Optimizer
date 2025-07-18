#!/usr/bin/env python3
import time, itertools
import numpy as np
import pandas as pd
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

# Número de repeticiones por punto
REPS = 5

def timed_solve(solver):
    # warm-up
    solver.solve()
    # repeticiones medidas
    ts = []
    for _ in range(REPS):
        start = time.perf_counter()
        solver.solve()
        ts.append(time.perf_counter() - start)
    return np.mean(ts)

def main():
    T_vals = [6,12,24]
    I_vals = [50,100,200]
    x_vals = [20,50,100]
    D_support = np.arange(11)
    D_probs   = np.full(11, 1/11)

    records = []
    for T,I_max,x_max in itertools.product(T_vals, I_vals, x_vals):
        dm = DemandModel(D_support, D_probs)
        solver = DynamicProgrammingSolver(
            T=T, I_max=I_max, x_max=x_max,
            costs={'c': np.full(T,10),'h':2,'p':20},
            demand_dist=dm
        )
        t_exec = timed_solve(solver)
        records.append({
            'T': T,
            'I_max': I_max,
            'x_max': x_max,
            'D_card': len(D_support),
            'T_exec': t_exec
        })
        print(f"T={T:<2} I={I_max:<3} x={x_max:<3} → {t_exec:.4f}s")

    df = pd.DataFrame(records)
    # regresión log-log solo en T, I_max y x_max
    y = np.log(df['T_exec'])
    X = np.column_stack([
        np.ones(len(df)),       # intercepto
        np.log(df['T']),        # exponente beta1
        np.log(df['I_max']),    # exponente beta2
        np.log(df['x_max'])     # exponente beta3
    ])
    β, *_ = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X.dot(β)
    R2 = 1 - ((y - y_pred)**2).sum()/((y - y.mean())**2).sum()

    print("\nCoeficientes (sin |D|):")
    names = ['α','β₁(logT)','β₂(logI)','β₃(logx)']
    for n,v in zip(names,β): print(f"  {n}: {v:.3f}")
    print(f"R² = {R2:.3f}")
    print("\nDatos:\n", df.to_string(index=False))

if __name__=="__main__":
    main()

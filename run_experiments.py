#!/usr/bin/env python3
import time
import numpy as np
import pandas as pd
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel


def main():
    # Parámetros comunes
    T = 12
    I_max = 100
    x_max = 50
    I0 = 0

    # Definición de escenarios
    scenarios = [
        {
            "Escenario": "Estacionario",
            "costs": {"c": np.full(T, 10), "h": 2, "p": 20},
            "support": np.arange(0, 11),
            "probs": np.full(11, 0.1)
        },
        {
            "Escenario": "Variable",
            "costs": {"c": 10 + 2 * np.sin(2 * np.pi * np.arange(T) / 12), "h": 2, "p": 20},
            "support": np.arange(0, 11),
            "probs": np.full(11, 1/11)
        },
        {
            "Escenario": "Sesgado",
            "costs": {"c": np.full(T, 10), "h": 2, "p": 50},
            "support": np.arange(0, 11),
            "probs": np.exp(-np.abs(np.arange(0, 11) - 5))
        }
    ]

    # Ahora normalizamos **todas** las distribuciones (no hace daño a las que ya suman 1):
    for esc in scenarios:
        esc["probs"] = esc["probs"] / esc["probs"].sum()

    resultados = []
    for esc in scenarios:
        dm = DemandModel(esc["support"], esc["probs"])
        solver = DynamicProgrammingSolver(
            T=T,
            I_max=I_max,
            x_max=x_max,
            costs=esc["costs"],
            demand_dist=dm
        )
        solver.solve()

        costo_opt = float(solver.V[0, I0])
        tiempo = solver.solution_time
        memoria_mb = solver.V.nbytes / (1024 * 1024)

        resultados.append({
            "Escenario": esc["Escenario"],
            "Costo Óptimo": costo_opt,
            "Tiempo (s)": tiempo,
            "Memoria (MB)": memoria_mb
        })

    df = pd.DataFrame(resultados)
    print("\nResultados de Optimalidad por Escenario (Tabla 7.1)\n")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()

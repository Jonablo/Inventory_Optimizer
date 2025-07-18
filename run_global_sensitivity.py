#!/usr/bin/env python3
"""
Análisis de Sensibilidad Global (Sección 8.3.3): Sobol indices para parámetros de costo.
"""
import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

# Definición del problema para SALib
problem = {
    'num_vars': 3,
    'names': ['c', 'h', 'p'],
    'bounds': [[5, 15],    # rango de c_t unitario
               [1, 5],     # rango de h
               [10, 50]]   # rango de p
}

# Generar muestras con Saltelli
param_values = saltelli.sample(problem, 512, calc_second_order=False)

# Preparar distribución base de demanda
support = list(range(11))
probs = [1/11] * 11

# Función objetivo: V0 dado un conjunto de parámetros
def evaluate(params):
    c_val, h_val, p_val = params
    # Costos constantes a lo largo del horizonte
    T = 12
    c_ts = np.full(T, c_val)
    dm = DemandModel(support, probs)
    solver = DynamicProgrammingSolver(
        T=T, I_max=100, x_max=50,
        costs={'c': c_ts, 'h': h_val, 'p': p_val},
        demand_dist=dm
    )
    V, _ = solver.solve()
    return V[0, 0]

# Evaluar el modelo sobre todas las muestras
y = np.array([evaluate(x) for x in param_values])

# Calcular índices de Sobol
ti = sobol.analyze(problem, y, calc_second_order=False)

# Mostrar resultados
print("Sobol first-order indices:")
for name, S1 in zip(problem['names'], ti['S1']):
    print(f"  S_{name}: {S1:.3f}")

print("\nSobol total-order indices:")
for name, ST in zip(problem['names'], ti['ST']):
    print(f"  ST_{name}: {ST:.3f}")

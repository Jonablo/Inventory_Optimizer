import numpy as np
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

def main():
    # Parámetros de ejemplo
    T, I_max, x_max = 3, 5, 5
    costs = {'c': np.array([1, 1, 1]), 'h': 2, 'p': 10}
    demand = DemandModel([0, 1, 2], [0.3, 0.4, 0.3])

    # Instanciar y resolver
    solver = DynamicProgrammingSolver(T, I_max, x_max, costs, demand)
    V, policy = solver.solve()

    # Mostrar resultados
    print("Value function V:")
    print(V)
    print("\nOptimal policy:")
    print(policy)

if __name__ == "__main__":
    main()
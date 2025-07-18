import numpy as np
import time

class DynamicProgrammingSolver:
    """
    Implementación del algoritmo de programación dinámica para
    optimización de inventario estocástico conforme al informe.
    """

    def __init__(self, T, I_max, x_max, costs: dict, demand_dist):
        """
        Args:
            T: Horizonte de planificación (int o float convertible)
            I_max: Nivel máximo de inventario (int o float convertible)
            x_max: Cantidad máxima de orden (int o float convertible)
            costs: Dict con {'c': secuencia de costos c_t, 'h': float, 'p': float}
            demand_dist: Objeto con métodos get_support() y get_probabilities()
        """
        # Asegurar que T, I_max y x_max sean enteros
        self.T = int(T)
        self.I_max = int(I_max)
        self.x_max = int(x_max)

        # Costos
        self.costs = costs['c']
        self.h = costs['h']
        self.p = costs['p']
        self.demand_dist = demand_dist

        # Tablas de memoización
        self.V = np.full((self.T + 1, self.I_max + 1), np.inf)
        self.policy = np.zeros((self.T, self.I_max + 1), dtype=int)
        self.solution_time = 0.0

    def solve(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Ejecuta el algoritmo de backward induction.
        Devuelve (V, policy).
        """
        start = time.time()
        # Condición terminal
        self.V[self.T, :] = 0

        # Recursión hacia atrás
        for t in range(self.T - 1, -1, -1):
            for I in range(self.I_max + 1):
                self._solve_state(t, I)

        self.solution_time = time.time() - start
        return self.V, self.policy

    def _solve_state(self, t: int, I: int):
        """
        Resuelve un estado (t, I) evaluando todas las acciones x.
        """
        min_cost = np.inf
        best_x = 0

        for x in range(min(self.x_max, self.I_max - I) + 1):
            cost = self._calculate_expected_cost(t, I, x)
            if cost < min_cost:
                min_cost = cost
                best_x = x

        self.V[t, I] = min_cost
        self.policy[t, I] = best_x

    def _calculate_expected_cost(self, t: int, I: int, x: int) -> float:
        """
        Calcula E[C_t + V_{t+1}] usando la distribución de demanda.
        """
        total = 0.0
        support = self.demand_dist.get_support()
        probs = self.demand_dist.get_probabilities()

        for D, p_D in zip(support, probs):
            I_next = I + x - D
            purchase_cost = self.costs[t] * x
            holding_cost = self.h * max(I_next, 0)
            shortage_cost = self.p * max(-I_next, 0)

            immediate = purchase_cost + holding_cost + shortage_cost
            future = self.V[t + 1, max(I_next, 0)]
            total += p_D * (immediate + future)

        return total

from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.cost_model import CostModel
from src.models.demand_model import DemandModel
from src.core.inventory_model import InventoryModel

class OptimizationEngine:
    """
    Orquesta la optimización completa conforme al diseño del informe:
    - Construye el solver de programación dinámica
    - Ejecuta solve() y devuelve resultados
    """

    def __init__(self,
                 I_init: int,
                 I_max: int,
                 x_max: int,
                 horizon: int,
                 c_ts: list[float],
                 h: float,
                 p: float,
                 demand_support: list[int],
                 demand_prob: list[float]):
        """
        Args:
            I_init: Inventario inicial
            I_max: Inventario máximo
            x_max: Pedido máximo
            horizon: Número de periodos T
            c_ts: Lista de costos unitarios de compra c_t, t=0..T-1
            h: Costo de almacenamiento
            p: Costo de penalización por escasez
            demand_support: Valores discretos d_i de demanda
            demand_prob: Probabilidades p_i (suman 1)
        """
        # Modelos
        self.inventory_model = InventoryModel(I_init, I_max, x_max)
        self.cost_model = CostModel(h, p)
        self.demand_model = DemandModel(demand_support, demand_prob)

        # Parámetros del solver
        costs = {'c': c_ts, 'h': h, 'p': p}
        self.solver = DynamicProgrammingSolver(
            T=horizon,
            I_max=I_max,
            x_max=x_max,
            costs=costs,
            demand_dist=self.demand_model
        )

    def run(self):
        """
        Ejecuta el solver y retorna:
            V: matriz de función de valor de tamaño (T+1)×(I_max+1)
            policy: matriz de política óptima de tamaño T×(I_max+1)
        """
        V, policy = self.solver.solve()
        return V, policy
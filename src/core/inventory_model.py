class InventoryModel:
    """
    Modelo de inventario según sección 1.2 del informe:
    - Estado: nivel de inventario I_t
    - Acciones factibles: 0 ≤ x_t ≤ x_max y I_t + x_t ≤ I_max
    - Transición de estados: I_{t+1} = I_t + x_t - D_t
    """

    def __init__(self, I_init: int, I_max: int, x_max: int):
        """
        Args:
            I_init: Inventario inicial I_0
            I_max: Inventario máximo permitido
            x_max: Cantidad máxima de pedido x_t
        """
        self.I_init = I_init
        self.I_max = I_max
        self.x_max = x_max

    def valid_actions(self, I: int) -> list[int]:
        """
        Devuelve la lista de acciones factibles A(t, I_t):
            x ∈ {0,1,...,x_max} tal que I + x ≤ I_max
        """
        return list(range(0, min(self.x_max, self.I_max - I) + 1))

    def state_transition(self, I: int, x: int, D: int) -> int:
        """
        Función de transición f(I_t, x_t, D_t) = I_t + x_t - D_t.
        Garantiza nivel no negativo: max(0, ...).
        """
        return max(I + x - D, 0)

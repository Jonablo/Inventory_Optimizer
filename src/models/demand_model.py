import numpy as np

class DemandModel:
    """
    Modelo de demanda discreta conforme al informe.
    """

    def __init__(self, support, probabilities):
        """
        Args:
            support: lista o np.ndarray de valores de demanda d_i
            probabilities: lista o np.ndarray de probabilidades p_i que suman 1
        """
        # Convertir a arrays de numpy
        self.support = np.array(support)
        self.probabilities = np.array(probabilities)

        # Validar suma de probabilidades con tolerancia
        total = self.probabilities.sum()
        if not np.isclose(total, 1.0, atol=1e-8):
            raise ValueError(f"Las probabilidades deben sumar 1 (suman {total}).")

    def get_support(self):
        return self.support

    def get_probabilities(self):
        return self.probabilities

import pytest
import numpy as np
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

def test_solver_constant_demand():
    T = 2
    I_max = 5
    x_max = 5
    costs = {'c': np.array([1, 1]), 'h': 0, 'p': 100}
    support = [1]
    probabilities = [1]
    demand = DemandModel(support, probabilities)
    solver = DynamicProgrammingSolver(T, I_max, x_max, costs, demand)
    V, policy = solver.solve()
    assert policy.shape == (T, I_max+1)

from flask import Flask, request, jsonify
from src.core.dynamic_programming_solver import DynamicProgrammingSolver
from src.models.demand_model import DemandModel

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    T = data['horizon']
    I_max = data['max_inventory']
    x_max = data['max_order']
    costs = data['costs']
    demand_params = data['demand_params']
    solver = DynamicProgrammingSolver(
        T=T,
        I_max=I_max,
        x_max=x_max,
        costs={'c': costs['c'], 'h': costs['h'], 'p': costs['p']},
        demand_dist=DemandModel(demand_params['support'], demand_params['probabilities'])
    )
    V, policy = solver.solve()
    result = {
        'value_function': V.tolist(),
        'policy': policy.tolist(),
        'solution_time': solver.solution_time
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

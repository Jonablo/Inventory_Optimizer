from flask import Blueprint, request, jsonify, abort
from datetime import datetime
import numpy as np

from src.core.optimization_engine import OptimizationEngine
from src.data.database_manager import (
    get_session, User, Material,
    Optimization, OptimalPolicy, OptimizationResult
)

optimization_bp = Blueprint('optimization', __name__)

@optimization_bp.route('/', methods=['POST'])
def run_optimization():
    """
    Ejecuta la optimización, persiste los resultados
    en la base de datos y devuelve JSON con optimization_id, value_function y policy.
    """
    data = request.get_json()
    session = get_session()

    # Asegurar existencia de usuario
    user_id = data.get('user_id', 1)
    user = session.get(User, user_id)
    if user is None:
        user = User(
            id=user_id,
            username=f'user{user_id}',
            email=f'user{user_id}@example.com',
            password_hash='',
            role='user'
        )
        session.add(user)
        session.commit()

    # Asegurar existencia de material
    material_id = data.get('material_id', 1)
    material = session.get(Material, material_id)
    if material is None:
        material = Material(
            id=material_id,
            name=f'material{material_id}',
            type='default',
            description='',
            unit_cost=0,
            storage_cost=0,
            shortage_penalty=0
        )
        session.add(material)
        session.commit()

    # Persistir registro de optimización
    opt = Optimization(
        user_id=user.id,
        material_id=material.id,
        name=data.get('name', 'AutoOpt'),
        horizon=data['horizon'],
        initial_inventory=data['initial_inventory'],
        max_inventory=data['max_inventory'],
        max_order=data['max_order'],
        costs=data['costs'],
        demand_params=data['demand_params'],
        status='running',
        created_at=datetime.utcnow()
    )
    session.add(opt)
    session.commit()

    # Ejecutar motor de optimización
    engine = OptimizationEngine(
        I_init=opt.initial_inventory,
        I_max=int(opt.max_inventory),
        x_max=int(opt.max_order),
        horizon=int(opt.horizon),
        c_ts=opt.costs['c'],
        h=opt.costs['h'],
        p=opt.costs['p'],
        demand_support=opt.demand_params['support'],
        demand_prob=opt.demand_params['probabilities']
    )
    V, policy = engine.run()

    # Persistir política óptima
    for t in range(policy.shape[0]):
        for I, x in enumerate(policy[t]):
            session.add(OptimalPolicy(
                optimization_id=opt.id,
                period=t,
                reorder_point=I if x > 0 else 0,
                order_up_to_level=I + int(x),
                expected_cost=float(V[t, I]),
                created_at=datetime.utcnow()
            ))
    session.commit()

    # Persistir resultados detallados
    demand_dist = engine.solver.demand_dist
    support = demand_dist.get_support()
    probs = demand_dist.get_probabilities()
    c_vec = np.array(opt.costs['c'])
    h = opt.costs['h']
    p_cost = opt.costs['p']

    for t in range(policy.shape[0]):
        for I in range(int(opt.max_inventory) + 1):
            x = int(policy[t, I])
            exp_demand = float(np.dot(support, probs))
            exp_holding = float(np.sum(probs * np.maximum(I + x - support, 0) * h))
            exp_shortage = float(np.sum(probs * np.maximum(support - (I + x), 0) * p_cost))
            purchase = float(c_vec[t] * x)
            total_period_cost = purchase + exp_holding + exp_shortage

            session.add(OptimizationResult(
                optimization_id=opt.id,
                period=t,
                inventory_level=float(I),
                optimal_order=float(x),
                expected_demand=exp_demand,
                expected_holding_cost=exp_holding,
                expected_shortage_cost=exp_shortage,
                total_period_cost=total_period_cost,
                created_at=datetime.utcnow()
            ))
    session.commit()

    # Marcar completada
    opt.status = 'completed'
    opt.solution_time = engine.solver.solution_time
    session.commit()

    return jsonify({
        'optimization_id': opt.id,
        'value_function': V.tolist(),
        'policy': policy.tolist()
    })


@optimization_bp.route('/<int:optimization_id>', methods=['GET'])
def get_optimization(optimization_id):
    session = get_session()
    opt = session.get(Optimization, optimization_id)
    if opt is None:
        abort(404, description='Optimization not found')

    completed_at_val = opt.completed_at
    completed_at_str = completed_at_val.isoformat() if completed_at_val is not None else None

    return jsonify({
        'optimization_id': opt.id,
        'name': opt.name,
        'status': opt.status,
        'total_cost': opt.total_cost,
        'solution_time': opt.solution_time,
        'created_at': opt.created_at.isoformat(),
        'completed_at': completed_at_str
    })


@optimization_bp.route('/<int:optimization_id>/policy', methods=['GET'])
def get_policy(optimization_id):
    session = get_session()
    policies: list[OptimalPolicy] = session.query(OptimalPolicy).filter_by(optimization_id=optimization_id).all()
    if len(policies) == 0:
        abort(404, description='Policy not found')
    return jsonify([
        {
            'period': p.period,
            'reorder_point': p.reorder_point,
            'order_up_to_level': p.order_up_to_level,
            'expected_cost': p.expected_cost
        }
        for p in policies
    ])


@optimization_bp.route('/<int:optimization_id>/results', methods=['GET'])
def get_results(optimization_id):
    session = get_session()
    results: list[OptimizationResult] = session.query(OptimizationResult).filter_by(optimization_id=optimization_id).all()
    if len(results) == 0:
        abort(404, description='Results not found')
    return jsonify([
        {
            'period': r.period,
            'inventory_level': r.inventory_level,
            'optimal_order': r.optimal_order,
            'expected_demand': r.expected_demand,
            'expected_holding_cost': r.expected_holding_cost,
            'expected_shortage_cost': r.expected_shortage_cost,
            'total_period_cost': r.total_period_cost
        }
        for r in results
    ])


@optimization_bp.route('/<int:optimization_id>/policy-summary', methods=['GET'])
def get_policy_summary(optimization_id):
    session = get_session()
    policies: list[OptimalPolicy] = session.query(OptimalPolicy).filter_by(optimization_id=optimization_id).all()
    if len(policies) == 0:
        abort(404, description='Policy not found')

    summary = []
    periods = sorted({p.period for p in policies})
    for t in periods:
        period_policies = [p for p in policies if p.period == t]
        # Solo consideramos los niveles de inventario con pedido > 0
        reorder_events = [p for p in period_policies if p.reorder_point > 0]  # type: ignore[reportGeneralTypeIssues]
        if len(reorder_events) == 0:
            s_t, S_t = None, None
        else:
            ev = min(reorder_events, key=lambda p: p.reorder_point)
            s_t, S_t = ev.reorder_point, ev.order_up_to_level
        summary.append({'period': t, 's_t': s_t, 'S_t': S_t})

    return jsonify(summary)

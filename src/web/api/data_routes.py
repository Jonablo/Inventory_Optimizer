from flask import Blueprint, request, jsonify

data_bp = Blueprint('data', __name__)

@data_bp.route('/historical', methods=['GET'])
def get_historical_demand():
    # lógica de datos...
    return jsonify([])

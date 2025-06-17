# app/routes/settlements.py
from flask import Blueprint, jsonify
from app.services.settlement_service import SettlementService

bp = Blueprint('settlements', __name__)

@bp.route('/balances', methods=['GET'])
def get_balances():
    """Get current balances for all people"""
    try:
        balances = SettlementService.calculate_balances()
        return jsonify({
            'success': True,
            'data': balances,
            'message': 'Balances calculated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error calculating balances: {str(e)}'
        }), 500

@bp.route('/settlements', methods=['GET'])
def get_settlements():
    """Get optimized settlement transactions"""
    try:
        settlements = SettlementService.calculate_settlements()
        return jsonify({
            'success': True,
            'data': settlements,
            'message': 'Settlements calculated successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error calculating settlements: {str(e)}'
        }), 500

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Get complete settlement summary"""
    try:
        summary = SettlementService.get_summary()
        return jsonify({
            'success': True,
            'data': summary,
            'message': 'Summary retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting summary: {str(e)}'
        }), 500
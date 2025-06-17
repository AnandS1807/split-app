# app/routes/settlements.py
from flask import Blueprint, jsonify, request
from app.services.settlement_service import SettlementService
from app.main import db


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
    
@bp.route('/settlements', methods=['POST'])
def add_settlement():
    try:
        data = request.get_json()
        settlement = Settlement(
            from_person=data['from_person'],
            to_person=data['to_person'],
            amount=data['amount'],
            notes=data.get('notes'),
            status=data.get('status', 'pending')
        )
        db.session.add(settlement)
        db.session.commit()
        
        return jsonify({
            'message': 'Settlement recorded successfully',
            'settlement': {
                'id': settlement.id,
                'from_person': settlement.from_person,
                'to_person': settlement.to_person,
                'amount': float(settlement.amount),
                'status': settlement.status
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/settlements/<int:settlement_id>', methods=['PUT'])
def update_settlement(settlement_id):
    try:
        settlement = Settlement.query.get_or_404(settlement_id)
        data = request.get_json()
        
        if 'status' in data:
            settlement.status = data['status']
        if 'notes' in data:
            settlement.notes = data['notes']
            
        db.session.commit()
        
        return jsonify({'message': 'Settlement updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
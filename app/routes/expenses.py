# app/routes/expenses.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.expense_service import ExpenseService
from app.utils.validators import ExpenseCreateSchema, ExpenseUpdateSchema

bp = Blueprint('expenses', __name__)

@bp.route('/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses"""
    try:
        expenses = ExpenseService.get_all_expenses()
        return jsonify({
            'success': True,
            'data': [expense.to_dict() for expense in expenses],
            'message': 'Expenses retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving expenses: {str(e)}'
        }), 500

@bp.route('/expenses', methods=['POST'])
def create_expense():
    """Create new expense"""
    try:
        schema = ExpenseCreateSchema()
        data = schema.load(request.json)
        
        expense = ExpenseService.create_expense(data)
        
        return jsonify({
            'success': True,
            'data': expense.to_dict(),
            'message': 'Expense added successfully'
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': 'Validation error',
            'errors': e.messages
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating expense: {str(e)}'
        }), 500

@bp.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """Get single expense"""
    try:
        expense = ExpenseService.get_expense(expense_id)
        return jsonify({
            'success': True,
            'data': expense.to_dict(),
            'message': 'Expense retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Expense not found: {str(e)}'
        }), 404

@bp.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update expense"""
    try:
        schema = ExpenseUpdateSchema()
        data = schema.load(request.json)
        
        expense = ExpenseService.update_expense(expense_id, data)
        
        return jsonify({
            'success': True,
            'data': expense.to_dict(),
            'message': 'Expense updated successfully'
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'message': 'Validation error',
            'errors': e.messages
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating expense: {str(e)}'
        }), 500

@bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete expense"""
    try:
        ExpenseService.delete_expense(expense_id)
        return jsonify({
            'success': True,
            'message': 'Expense deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting expense: {str(e)}'
        }), 500

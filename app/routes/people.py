# app/routes/people.py
from flask import Blueprint, jsonify, request
from app.models.person import Person
from app.main import db
from app.models.expense import Expense

bp = Blueprint('people', __name__)

@bp.route('/people', methods=['GET'])
def get_people():
    """Get all people"""
    try:
        people = Person.query.order_by(Person.name).all()
        return jsonify({
            'success': True,
            'data': [person.to_dict() for person in people],
            'message': 'People retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving people: {str(e)}'
        }), 500
@bp.route('/people', methods=['POST'])
def add_person():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
            
        # Check if person already exists
        existing_person = Person.query.filter_by(name=name).first()
        if existing_person:
            return jsonify({'error': 'Person already exists in the group'}), 400
            
        # Create new person
        new_person = Person(name=name)
        db.session.add(new_person)
        db.session.commit()
        
        return jsonify({
            'message': f'{name} added to the group successfully',
            'person': {
                'id': new_person.id,
                'name': new_person.name
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@bp.route('/people/<int:person_id>', methods=['DELETE'])
def remove_person(person_id):
    try:
        person = Person.query.get_or_404(person_id)
        
        # Check if person has any expenses
        expense_count = Expense.query.filter_by(paid_by=person.name).count()
        if expense_count > 0:
            return jsonify({
                'error': f'Cannot remove {person.name} - they have {expense_count} expenses. Please settle or transfer expenses first.'
            }), 400
            
        db.session.delete(person)
        db.session.commit()
        
        return jsonify({'message': f'{person.name} removed from the group'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
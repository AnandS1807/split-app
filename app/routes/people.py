# app/routes/people.py
from flask import Blueprint, jsonify
from app.models.person import Person

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

# app/services/settlement_service.py
from app.models.person import Person
from app.models.expense import Expense, ExpenseSplit
from decimal import Decimal
from collections import defaultdict

class SettlementService:
    @staticmethod
    def calculate_balances():
        """Calculate how much each person owes or is owed"""
        people = Person.query.all()
        balances = {}
        
        for person in people:
            # Calculate total paid by this person
            total_paid = sum(
                float(expense.amount) for expense in person.expenses_paid
            )
            
            # Calculate total owed by this person (their share of all expenses)
            total_owed = sum(
                float(split.split_amount) for split in person.expense_splits
            )
            
            # Net balance: positive means they are owed money, negative means they owe money
            net_balance = total_paid - total_owed
            
            balances[person.name] = {
                'person_id': person.id,
                'person_name': person.name,
                'total_paid': round(total_paid, 2),
                'total_owed': round(total_owed, 2),
                'net_balance': round(net_balance, 2),
                'status': 'owed' if net_balance > 0 else 'owes' if net_balance < 0 else 'settled'
            }
        
        return balances
    
    @staticmethod
    def calculate_settlements():
        """Calculate optimized settlements to minimize transactions"""
        balances = SettlementService.calculate_balances()
        
        # Separate creditors (people who are owed money) and debtors (people who owe money)
        creditors = []
        debtors = []
        
        for person_name, balance_info in balances.items():
            net_balance = balance_info['net_balance']
            if net_balance > 0:
                creditors.append({
                    'name': person_name,
                    'amount': net_balance
                })
            elif net_balance < 0:
                debtors.append({
                    'name': person_name,
                    'amount': abs(net_balance)
                })
        
        # Sort creditors and debtors by amount (largest first)
        creditors.sort(key=lambda x: x['amount'], reverse=True)
        debtors.sort(key=lambda x: x['amount'], reverse=True)
        
        settlements = []
        i, j = 0, 0
        
        # Match creditors with debtors
        while i < len(creditors) and j < len(debtors):
            creditor = creditors[i]
            debtor = debtors[j]
            
            # Calculate settlement amount
            settlement_amount = min(creditor['amount'], debtor['amount'])
            
            if settlement_amount > 0:
                settlements.append({
                    'from': debtor['name'],
                    'to': creditor['name'],
                    'amount': round(settlement_amount, 2)
                })
                
                # Update remaining amounts
                creditor['amount'] -= settlement_amount
                debtor['amount'] -= settlement_amount
            
            # Move to next creditor or debtor if current one is settled
            if creditor['amount'] == 0:
                i += 1
            if debtor['amount'] == 0:
                j += 1
        
        return settlements
    
    @staticmethod
    def get_summary():
        """Get complete settlement summary"""
        balances = SettlementService.calculate_balances()
        settlements = SettlementService.calculate_settlements()
        
        # Calculate totals
        total_expenses = sum(
            float(expense.amount) for expense in Expense.query.all()
        )
        
        people_count = len(balances)
        
        return {
            'total_expenses': round(total_expenses, 2),
            'people_count': people_count,
            'balances': balances,
            'settlements': settlements,
            'settlement_count': len(settlements)
        }

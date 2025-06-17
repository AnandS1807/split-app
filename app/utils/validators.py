# app/utils/validators.py
from marshmallow import Schema, fields, validate, ValidationError

class ExpenseCreateSchema(Schema):
    amount = fields.Decimal(required=True, validate=validate.Range(min=0.01), places=2)
    description = fields.String(required=True, validate=validate.Length(min=1, max=255))
    paid_by = fields.String(required=True, validate=validate.Length(min=1, max=100))
    split_type = fields.String(missing='equal', validate=validate.OneOf(['equal', 'percentage', 'exact']))
    splits = fields.List(fields.Dict(), missing=None)

class ExpenseUpdateSchema(Schema):
    amount = fields.Decimal(validate=validate.Range(min=0.01), places=2)
    description = fields.String(validate=validate.Length(min=1, max=255))
    paid_by = fields.String(validate=validate.Length(min=1, max=100))

# app/services/expense_service.py
from app.main import db
from app.models.person import Person
from app.models.expense import Expense, ExpenseSplit
from decimal import Decimal

class ExpenseService:
    @staticmethod
    def create_expense(data):
        """Create a new expense and automatically handle person creation"""
        # Get or create person
        person = Person.query.filter_by(name=data['paid_by']).first()
        if not person:
            person = Person(name=data['paid_by'])
            db.session.add(person)
            db.session.commit()
        
        # Create expense
        expense = Expense(
            amount=Decimal(str(data['amount'])),
            description=data['description'],
            paid_by_id=person.id
        )
        db.session.add(expense)
        db.session.commit()
        
        # Create equal splits for all people by default
        ExpenseService._create_equal_splits(expense)
        
        return expense
    
    @staticmethod
    def _create_equal_splits(expense):
        """Create equal splits for all people in the system"""
        all_people = Person.query.all()
        if not all_people:
            return
        
        split_amount = expense.amount / len(all_people)
        
        for person in all_people:
            split = ExpenseSplit(
                expense_id=expense.id,
                person_id=person.id,
                split_amount=split_amount,
                split_type='equal'
            )
            db.session.add(split)
        
        db.session.commit()
    
    @staticmethod
    def update_expense(expense_id, data):
        """Update existing expense"""
        expense = Expense.query.get_or_404(expense_id)
        
        if 'amount' in data:
            expense.amount = Decimal(str(data['amount']))
        if 'description' in data:
            expense.description = data['description']
        if 'paid_by' in data:
            person = Person.query.filter_by(name=data['paid_by']).first()
            if not person:
                person = Person(name=data['paid_by'])
                db.session.add(person)
                db.session.commit()
            expense.paid_by_id = person.id
        
        db.session.commit()
        
        # Recalculate splits if amount changed
        if 'amount' in data:
            # Delete existing splits
            ExpenseSplit.query.filter_by(expense_id=expense.id).delete()
            # Create new equal splits
            ExpenseService._create_equal_splits(expense)
        
        return expense
    
    @staticmethod
    def delete_expense(expense_id):
        """Delete expense and its splits"""
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        return True
    
    @staticmethod
    def get_all_expenses():
        """Get all expenses with details"""
        return Expense.query.order_by(Expense.created_at.desc()).all()
    
    @staticmethod
    def get_expense(expense_id):
        """Get single expense by ID"""
        return Expense.query.get_or_404(expense_id)
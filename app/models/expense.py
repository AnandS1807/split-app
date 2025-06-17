# app/models/expense.py
from app.main import db
from datetime import datetime
from decimal import Decimal

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    paid_by_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    splits = db.relationship('ExpenseSplit', backref='expense', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Expense {self.description}: {self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'description': self.description,
            'paid_by': self.payer.name,
            'paid_by_id': self.paid_by_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'splits': [split.to_dict() for split in self.splits]
        }

class ExpenseSplit(db.Model):
    __tablename__ = 'expense_splits'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    split_amount = db.Column(db.Numeric(10, 2), nullable=False)
    split_type = db.Column(db.String(20), default='equal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExpenseSplit {self.person.name}: {self.split_amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_name': self.person.name,
            'person_id': self.person_id,
            'split_amount': float(self.split_amount),
            'split_type': self.split_type
        }
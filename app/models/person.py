# app/models/person.py
from app.main import db
from datetime import datetime

class Person(db.Model):
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses_paid = db.relationship('Expense', backref='payer', lazy=True)
    expense_splits = db.relationship('ExpenseSplit', backref='person', lazy=True)
    
    def __repr__(self):
        return f'<Person {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

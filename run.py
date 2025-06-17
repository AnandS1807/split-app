# run.py
from app.main import create_app, db
from app.models.person import Person
from app.models.expense import Expense, ExpenseSplit

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Person': Person,
        'Expense': Expense,
        'ExpenseSplit': ExpenseSplit
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
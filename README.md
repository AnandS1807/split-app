A robust backend system for splitting expenses among groups of people, built with Flask and PostgreSQL.

## Features

### Core Features (MUST HAVE)
- **Expense Tracking**: Add, edit, delete, and view expenses
- **Auto Person Management**: People are automatically added when mentioned in expenses
- **Settlement Calculations**: Smart algorithm to minimize transactions
- **Balance Tracking**: See who owes what to whom
- **Input Validation**: Comprehensive validation and error handling
- **RESTful API**: Clean, consistent API design

### API Endpoints

#### Expense Management
- `GET /api/expenses` - List all expenses
- `POST /api/expenses` - Add new expense
- `GET /api/expenses/:id` - Get specific expense
- `PUT /api/expenses/:id` - Update expense
- `DELETE /api/expenses/:id` - Delete expense

#### Settlement & Balance
- `GET /api/balances` - Get current balances for all people
- `GET /api/settlements` - Get optimized settlement transactions
- `GET /api/summary` - Get complete summary with totals

#### People Management
- `GET /api/people` - List all people (auto-populated from expenses)

#### Health Check
- `GET /health` - API health status

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Marshmallow
- **Deployment**: Railway.app
- **Testing**: Postman

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd split-app-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
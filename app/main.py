# app/main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.expenses import bp as expenses_bp
    from app.routes.settlements import bp as settlements_bp
    from app.routes.people import bp as people_bp
    
    app.register_blueprint(expenses_bp, url_prefix='/api')
    app.register_blueprint(settlements_bp, url_prefix='/api')
    app.register_blueprint(people_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Split App API is running'}
    
    return app
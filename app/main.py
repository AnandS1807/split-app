# app/main.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    try:
        app.config.from_object(Config)
        logger.info(f"Database URL configured: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
        
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
            try:
                # Test database connection
                db.engine.execute('SELECT 1')
                db_status = 'connected'
            except Exception as e:
                logger.error(f"Database connection failed: {str(e)}")
                db_status = 'disconnected'
            
            return {
                'status': 'healthy', 
                'message': 'Split App API is running',
                'database': db_status,
                'port': os.environ.get('PORT', 'Not set')
            }
        
        @app.route('/')
        def index():
            return render_template('index.html')
        
        @app.route('/expenses')
        def expenses_page():
            return render_template('expenses.html')
        
        @app.route('/settlements')
        def settlements_page():
            return render_template('settlements.html')
        
        logger.info("Flask app created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to create Flask app: {str(e)}")
        raise
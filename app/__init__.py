from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration from config.py
    app.config.from_object(config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp, crops_bp, labour_bp, costs_bp, reports_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(crops_bp)
    app.register_blueprint(labour_bp)
    app.register_blueprint(costs_bp)
    app.register_blueprint(reports_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

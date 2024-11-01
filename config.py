import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize SQLAlchemy without an app context
db = SQLAlchemy()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')  # Use an environment variable for security
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking to save resources
    SQLALCHEMY_ECHO = False  # Set to True to see raw SQL queries in debug mode

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'user_management.db')}"

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'test_user_management.db')}"
    SQLALCHEMY_ECHO = True  # Helpful to see SQL logs during testing

class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'prod_user_management.db')}")
    DEBUG = False
    TESTING = False

# Configuration dictionary for easy access
configurations = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def create_app(config_name='default'):
    """App factory function to initialize the app with a configuration."""
    app = Flask(__name__)
    app.config.from_object(configurations[config_name])

    # Initialize SQLAlchemy with app context
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

# Create an app instance with the default configuration
app = create_app()

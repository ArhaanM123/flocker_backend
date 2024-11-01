import os

basedir = os.path.abspath(os.path.dirname(__file__))

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
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

import os

# The 'config.py' file contains configuration settings for your project, 
# including database connections, API keys, and other environment-specific variables.

class Config:
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')  # 'fallback_secret_key' if not set
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'fallback_weather_api_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///idms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    TESTING = False
    
    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///idms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'd3437b12773eb0feaeba59084f496eeb')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///idms.db')

# Mapping for configuration environments
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


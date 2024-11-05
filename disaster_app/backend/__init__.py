from flask import Flask
from .models import db
from .routes import main_bp

def create_app():
    app = Flask(__name__,
                template_folder="../frontend/templates",  # Explicit path to templates folder
                static_folder="../frontend/static")       # Explicit path to static folder

    app.config.from_object('config.Config')  # Adjust this based on your config
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    return app

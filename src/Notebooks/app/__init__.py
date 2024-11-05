# app/__init__.py

from flask import Flask
from config import Config

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Import and register blueprints or routes
from app.backend import routes

# Example: Register the routes blueprint
app.register_blueprint(routes.bp)

# You can also set up other things like database initialization here
# from app.backend.models import db
# db.init_app(app)

from flask import Flask, render_template, request, flash, jsonify, redirect, url_for
from dotenv import load_dotenv
import os
import secrets
from flask_sqlalchemy import SQLAlchemy
import sys

# Add necessary paths to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config import config
from disaster_app.backend.routes import main_bp
from disaster_app.backend.models import db

# Initialize Flask app
app = Flask(__name__,
            template_folder="../frontend/templates",  # Explicit path to templates folder
            static_folder="../frontend/static")       # Explicit path to static folder

# Set a secret key
app.secret_key = secrets.token_hex(16)

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Load configuration from config.py
app.config.from_object(config['development'])

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///idms.db'  # Fallback to SQLite if not set
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Register the Blueprint
app.register_blueprint(main_bp)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Dummy check (replace this with actual logic)
        if username != 'admin' or password != 'password':
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        
        # If login is successful
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Debug route for environment variables
@app.route('/debug')
def debug():
    secret_key = os.getenv('SECRET_KEY', 'No Secret Key Found')
    api_key = os.getenv('WEATHER_API_KEY', 'No Weather API Key Found')
    return f"Secret Key: {secret_key}, Weather API Key: {api_key}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

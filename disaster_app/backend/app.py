from flask import Flask, render_template, request, flash, jsonify, redirect, url_for
from dotenv import load_dotenv
from flask_migrate import Migrate

import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import sys
import requests
import secrets
import json
import re  # For email validation
import joblib
import sklearn

from disaster_app.backend.routes import main_bp
from disaster_app.backend.models import db, DisasterEvent, Prediction
from src.idms_functions import clean_data, create_features, generate_alert, suggest_action, fetch_live_data
from config import config

# Add the src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Add the root folder to Python path (for config.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Initialize Flask app
app = Flask(__name__,
            template_folder="../frontend/templates",
            static_folder="../frontend/static")

# Generate a random secret key for Flask sessions
app.secret_key = secrets.token_hex(16)

# Load environment variables from the .env file
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

if not WEATHER_API_KEY:
    raise ValueError("Weather API key is not set!")

# Load configuration from config.py
app.config.from_object(config['development'])
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///idms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create tables on the first request using the correct decorator
@app.before_request
def create_tables():
    db.create_all()

# Register the Blueprint
app.register_blueprint(main_bp)

# Home route
@app.route('/')
def home():
    return render_template('index.html')


# home route
@app.route('/home1')
def home1():
    return render_template('index.html')
# Mock user data
users = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # Added email field
        password = request.form.get('password')

        # Check if all fields are filled
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('login'))

        # Check for existing user credentials
        for user in users:
            if user['username'] == username and user['password'] == password and user['email'] == email:
                flash('Login successful!', 'success')
                return redirect(url_for('home'))

        # If no match found, create a new user entry
        users.append({'username': username, 'email': email, 'password': password})
        flash('New user created and logged in successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Settings route
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
    username = "default_user"  # Replace this with a dynamic username from the session

    if request.method == 'POST':
        # Get the form data
        alert_threshold = request.form.get('alert_threshold')
        email_notifications = request.form.get('email_notifications') == 'on'  # Convert "on" to boolean
        username = request.form.get('username')
        email = request.form.get('email')

        print(f"Received data: {username}, {email}, {alert_threshold}, {email_notifications}")

        # Check if username and email are provided
        if not username or not email:
            flash('Username and email are required!', 'error')
            return redirect(url_for('settings'))

        # Load existing settings from the file if it exists
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                try:
                    settings_data = json.load(f)
                except json.JSONDecodeError:
                    settings_data = {}
        else:
            settings_data = {}

        # Update the settings for the current user
        settings_data[username] = {
            'email': email,
            'alert_threshold': alert_threshold,
            'email_notifications': email_notifications
        }

        # Save the updated settings back to the file
        with open(settings_file, 'w') as f:
            json.dump(settings_data, f, indent=4)

        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))

    else:
        # GET request: Load existing settings for the current user
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                try:
                    settings_data = json.load(f)
                except json.JSONDecodeError:
                    settings_data = {}
        else:
            settings_data = {}

        # Get the specific settings for the current user (if they exist)
        user_settings = settings_data.get(username, {})

    # Render the settings page, passing the user settings to the template
    return render_template('settings.html', settings=user_settings)

@app.route('/test_data')
def test_data():
    events = DisasterEvent.query.all()
    alerts = Alert.query.all()
    return jsonify({
        'events': [event.name for event in events],
        'alerts': [alert.message for alert in alerts]
    })

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    location = None
    if request.method == 'POST':
        # User input ko receive karein
        location = request.form.get('location')
        
        # Terminal mein location print karein
        print(f"Entered Location: {location}")
    
    return render_template('dashboard.html', location=location)


def weather1(api_key, city):
    # OpenWeather API endpoint for current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        # Make a request to the OpenWeather API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        # Extract weather description
        weather_description = data['weather'][0]['description']
        return weather_description

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_weather_data(location, api_key):
    """Fetch weather keywords, location, and description for a given location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    
    # Send GET request to OpenWeather API
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        
        # Extracting weather condition
        weather_description = str(weather_data['weather'][0]['description'])
        
        # Generate keywords based on the weather description
        keywords = []
        if "rain" in weather_description:
            keywords.append("rainy")
        if "cloud" in weather_description:
            keywords.append("cloudy")
        if "clear" in weather_description:
            keywords.append("sunny")
        if "storm" in weather_description:
            keywords.append("stormy")
        if "snow" in weather_description:
            keywords.append("snowy")
        keywords=weather_description
        return {
        'keyword': [keywords],
        'location': [location],
        'text': [weather_description]
    }
    else:
        print("Error fetching data from OpenWeather API.")
        return None


@app.route('/generate_predict', methods=['POST'])
def generate_predict():
    print("Form submission received", flush=True)

    # Fetch the form data (ensure the form action matches this route)
    location = request.form.get('location')

   
    
    # Perform your prediction logic (e.g., disaster prediction)
    preprocess=fetch_weather_data(location, WEATHER_API_KEY)

    #load and predict model
    model=joblib.load('Data/models/pipeline.pkl')
    # data = pd.read_csv("Data/raw_data/train.csv")

    input_df = pd.DataFrame(preprocess)

    # Use the pipeline to make predictions
   

    res = model.predict(input_df)
   



    prediction = f"Prediction generated for {location} is {preprocess["keyword"]} : {res}"
    
    # Optionally, print to terminal for debugging
    print(f"Location entered: {location}",  flush=True)
    
    # Return a response (e.g., render a template or return JSON)
    return render_template('dashboard.html', prediction=prediction)



# Alerts route
@app.route('/alerts')
def Alert():
    return render_template('alert.html')

# Debug route to check environment variables
@app.route('/debug')
def debug():
    secret_key = os.getenv('SECRET_KEY', 'No Secret Key Found')
    api_key = os.getenv('WEATHER_API_KEY', 'No Weather API Key Found')
    return f"Secret Key: {secret_key}, Weather API Key: {api_key}"

# Function to get weather data from OpenWeatherMap API
def get_weather(city):
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

# Route to fetch weather data for a specific city
@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')  # Get the city from query parameters
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    weather_data = get_weather(city)
    return jsonify(weather_data)

# Route to fetch live weather data and process it
@app.route('/fetch_weather', methods=['GET'])
def fetch_weather():
    try:
        weather_data = fetch_live_data(WEATHER_API_KEY)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Example of processing the data
    weather_df = pd.DataFrame([weather_data])
    cleaned_data = clean_data(weather_df)
    features = create_features(cleaned_data)

    return jsonify(features.to_dict())

# Route for model prediction and decision support
@app.route('/predict', methods=['POST'])
def predict():
    # Assume incoming data in JSON format
    data = request.json
    df = pd.DataFrame(data)

    # Clean and process the data
    cleaned_data = clean_data(df)
    features = create_features(cleaned_data)

    # Example model prediction (replace with your model prediction code)
    prediction = 0.36  # Replace with model.predict(features)

    # Generate alert and suggest action
    alert = generate_alert(prediction)
    action = suggest_action(prediction)

    return jsonify({
        'prediction': prediction,
        'alert': alert,
        'action': action
    })





# Run the app
if __name__ == '__main__':
    app.run(debug=True)

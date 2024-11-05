from flask import Flask, request, jsonify
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from backend.models import db, DisasterEvent, Prediction  # Import the database and models
from backend.routes import main_bp  # Import the Blueprint
from src.idms_functions import clean_data, create_features, generate_alert, suggest_action, fetch_live_weather_data

app = Flask(__name__)

# Configuring the database URI (example: SQLite, replace with your DB URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///disaster_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register the Blueprint
app.register_blueprint(main_bp)

# Create the database tables (Run once)
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return "Welcome to the Intelligence Disaster Management System!"

# Route to fetch live weather data and process it
@app.route('/fetch_weather', methods=['GET'])
def fetch_weather():
    api_url = "https://api.example.com/weather"  # Replace with actual API URL
    weather_data = fetch_live_weather_data(api_url)
    
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
    prediction = 0.8  # Replace with model.predict(features)
    
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

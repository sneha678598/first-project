# routes.py ka code 
import sys
import os
import json
from flask import Blueprint, jsonify, request
from src.idms_functions import fetch_live_data, suggest_action, generate_alert

# Ensure the src folder is in the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Create a Blueprint for your routes
main_bp = Blueprint('main', __name__)

# Load API key securely from environment variables
api_key = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Route for fetching live weather data
@main_bp.route('/fetch_weather/<city>', methods=['GET'])
def fetch_weather(city):
    try:
        api_url = f"{BASE_URL}?q={city}&appid={api_key}"
        # Fetch live data
        fetch_live_data(api_url, 'data/live_data/live_data.json')
        
        # Read the fetched data
        live_data_file = os.path.join('data', 'live_data', 'live_data.json')
        with open(live_data_file, 'r') as file:
            live_data = json.load(file)
        
        return jsonify(live_data), 200
    except FileNotFoundError:
        return jsonify({'error': 'Live data file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for suggesting action based on prediction
@main_bp.route('/suggest_action', methods=['POST'])
def suggest_action_route():
    try:
        data = request.json
        prediction = data.get('prediction', 0.0)
        action = suggest_action(prediction)
        return jsonify({'suggested_action': action}), 200
    except KeyError:
        return jsonify({'error': 'Prediction not provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for generating alerts
@main_bp.route('/generate_alert', methods=['POST'])
def generate_alert_route():
    try:
        data = request.json
        prediction = data.get('prediction', 0.0)
        generate_alert(prediction)
        return jsonify({'message': 'Alert generated if prediction exceeds threshold'}), 200
    except KeyError:
        return jsonify({'error': 'Prediction not provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500#
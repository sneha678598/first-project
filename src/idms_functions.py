# idms_functions.py

import pandas as pd
import requests
import json
import os
import joblib

# File paths
live_data_file = os.path.join('..', 'data', 'live_data', 'live_data.json')  # Save fetched live data
model_path = os.path.join('..', 'data', 'models', 'pipeline.pkl')  # Path to the trained model
predictions_file = os.path.join('..', 'data', 'processed_data', 'live_data_predictions.csv')  # Save predictions

# Data Processing Functions
def clean_data(df):
    # Example cleaning: remove missing values
    df = df.dropna()
    return df

# Feature Engineering Functions
def create_features(df):
    # Example feature: Create a new feature by doubling an existing feature (if present)
    if 'existing_feature' in df.columns:
        df['new_feature'] = df['existing_feature'] * 2
    return df

# Alert Functions
def generate_alert(prediction, threshold=0.7):
    # Generate an alert based on a prediction value and threshold
    if prediction > threshold:
        print("Alert: High Risk Detected!")

# Decision Support Functions
def suggest_action(prediction, threshold=0.7):
    # Suggest actions based on the prediction value
    if prediction > threshold:
        return "Evacuate Area"
    else:
        return "Monitor Situation"

# Fetch Live Data from API
def fetch_live_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            live_data = response.json()
            with open(live_data_file, 'w') as file:
                json.dump(live_data, file, indent=4)
            print("Live data fetched and saved successfully.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching live data: {e}")

# Process the Live Data and Make Predictions
def process_live_data():
    if os.path.exists(live_data_file):
        try:
            # Load the live data
            with open(live_data_file, 'r') as file:
                live_data = json.load(file)
            
            # Extract required fields
            location = live_data.get('name', 'Unknown')
            keyword = live_data['weather'][0]['main'].lower()
            text = f"The weather in {location} is {live_data['weather'][0]['description']}."
            
            # Create DataFrame for processing
            live_data_df = pd.DataFrame([{
                'keyword': keyword,
                'location': location,
                'text': text
            }])
            
            # Preprocess the data: clean and feature engineering
            live_data_df = clean_data(live_data_df)
            live_data_df = create_features(live_data_df)

            # Load the trained model pipeline
            pipeline = joblib.load(model_path)
            
            # Preprocess and predict
            live_data_processed = pipeline.named_steps['preprocessor'].transform(live_data_df)
            predictions = pipeline.named_steps['model'].predict(live_data_processed)

            # Generate alert based on prediction
            for prediction in predictions:
                generate_alert(prediction)

            # Suggest actions based on predictions
            for prediction in predictions:
                action = suggest_action(prediction)
                print(f"Suggested Action: {action}")

            # Save predictions to CSV
            pd.DataFrame(predictions, columns=['prediction']).to_csv(predictions_file, index=False)
            print("Live data processed and predictions saved successfully.")
        
        except Exception as e:
            print(f"An error occurred during processing: {e}")
    else:
        print(f"File not found: {live_data_file}")

if __name__ == "__main__":
    # Example of fetching and processing live weather data
    api_key = 'd3437b12773eb0feaeba59084f496eeb'
    city_name = 'London'
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    
    fetch_live_data(api_url)   # Fetch new live data
    process_live_data()        # Process the fetched data and make predictions

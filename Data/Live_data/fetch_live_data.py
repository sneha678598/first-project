import requests
import os
import json  

# Define the directory path for saving live data
live_data_path = r'C:\Users\acer\Disaster_management_system\Data\Live_data\\'



# Ensure the directory exists
os.makedirs(live_data_path, exist_ok=True)

# Function to fetch live data from an API
def fetch_live_data(api_url, save_file_name):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()  # Assuming the API returns JSON data
        
        # Save the fetched data to a file
        file_path = f'{live_data_path}{save_file_name}'
        with open(file_path, 'w') as file:
            json.dump(data, file)
        
        print(f"Live data saved successfully to '{file_path}'.")
    else:
        print(f"Failed to fetch live data. Status code: {response.status_code}")

# Example usage
api_key = 'd3437b12773eb0feaeba59084f496eeb'
api_url = f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}'
save_file_name = 'live_data.json'
fetch_live_data(api_url, save_file_name)

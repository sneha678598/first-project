// main.js

// Function to fetch live data and update the UI
async function fetchLiveData() {
    try {
        const response = await fetch('/live-data'); // API endpoint to fetch live data
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        updateUI(data); // Function to update the UI with the fetched data
    } catch (error) {
        console.error('Failed to fetch live data:', error);
        showError('Failed to fetch live data. Please try again later.');
    }
}

// Function to update the UI with live data
function updateUI(data) {
    const weatherElement = document.getElementById('weather-info');

    // Check if required properties exist
    if (data.city_name && data.temperature && data.weather_description && data.wind_speed && data.humidity) {
        weatherElement.innerHTML = `
            <h3>Weather in ${data.city_name}</h3>
            <p>Temperature: ${data.temperature}°C</p>
            <p>Condition: ${data.weather_description}</p>
            <p>Wind Speed: ${data.wind_speed} m/s</p>
            <p>Humidity: ${data.humidity}%</p>
        `;
    } else {
        showError('Data is missing or in an incorrect format.');
    }
}

// Function to show error messages
function showError(message) {
    const weatherElement = document.getElementById('weather-info');
    weatherElement.innerHTML = `<p style="color: red;">${message}</p>`;
}

// Event listener for page load
document.addEventListener('DOMContentLoaded', () => {
    fetchLiveData(); // Fetch live data when the page loads
});

// Optional: Set an interval to refresh live data periodically
setInterval(fetchLiveData, 60000); // Fetch live data every 60 seconds

// main.js

// Function to toggle the navigation menu
function toggleMenu() {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('active');
}

// Event listener for menu toggle button
document.querySelector('.menu-toggle').addEventListener('click', toggleMenu);

// Function to fetch live weather data
async function fetchWeatherData(location) {
    try {
        const response = await fetch(`/api/weather?location=${location}`);
        const data = await response.json();
        displayWeatherData(data);
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

// Function to display weather data on the page
function displayWeatherData(data) {
    const weatherElement = document.querySelector('.weather-info');
    weatherElement.innerHTML = `
        <h3>Weather for ${data.location}</h3>
        <p>Temperature: ${data.temperature}°C</p>
        <p>Condition: ${data.condition}</p>
    `;
}

// Example: Fetch and display weather data for a default location
fetchWeatherData('New York');

// Function to handle alert notifications
function handleAlerts(alerts) {
    const alertsContainer = document.querySelector('.alerts-container');
    alerts.forEach(alert => {
        const alertElement = document.createElement('div');
        alertElement.className = 'alert';
        alertElement.innerHTML = `
            <h4>${alert.title}</h4>
            <p>${alert.message}</p>
        `;
        alertsContainer.appendChild(alertElement);
    });
}

// Fetch alerts from the server
async function fetchAlerts() {
    try {
        const response = await fetch('/api/alerts');
        const alerts = await response.json();
        handleAlerts(alerts);
    } catch (error) {
        console.error('Error fetching alerts:', error);
    }
}

// Initialize alerts on page load
fetchAlerts();

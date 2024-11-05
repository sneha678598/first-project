// alerts.js

/// Function to display alerts based on risk levels
function displayAlert(message, type) {
    const alertContainer = document.getElementById('alert-container');

    // Check if the alert already exists
    const existingAlerts = alertContainer.getElementsByClassName(type);
    if (existingAlerts.length > 0) {
        return; // Avoid displaying duplicate alerts of the same type
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${type}`;
    alertDiv.textContent = message;

    // Add close button to the alert
    const closeButton = document.createElement('button');
    closeButton.textContent = '×';
    closeButton.className = 'close-btn';
    closeButton.onclick = () => {
        alertContainer.removeChild(alertDiv);
    };

    alertDiv.appendChild(closeButton);
    alertContainer.appendChild(alertDiv);
}

// Function to check risk levels and trigger alerts
function checkRiskLevels(data) {
    if (data.riskLevel === 'high') {
        displayAlert('High Risk Detected! Evacuate immediately!', 'alert-danger');
    } else if (data.riskLevel === 'medium') {
        displayAlert('Medium Risk: Stay Alert!', 'alert-warning');
    } else {
        displayAlert('Low Risk: All Clear.', 'alert-success');
    }
}

// Example function to fetch and evaluate alerts
async function fetchAlerts() {
    const response = await fetch('/alerts'); // API endpoint to fetch alerts
    if (response.ok) {
        const data = await response.json();
        checkRiskLevels(data); // Check risk levels based on fetched data
    } else {
        console.error('Failed to fetch alerts:', response.statusText); // Improved error handling
    }
}

// Event listener for page load
document.addEventListener('DOMContentLoaded', () => {
    fetchAlerts(); // Fetch alerts when the page loads
});

// Optional: Set an interval to refresh alerts periodically
setInterval(fetchAlerts, 300000); // Fetch alerts every 5 minutes

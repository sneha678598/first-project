// alerts.js

// Function to generate alert notifications based on data
function generateAlert(alertType, message) {
    const alertBox = document.createElement('div');
    alertBox.className = `alert ${alertType}`;
    alertBox.innerText = message;
    
    // Append alert to the alert container
    const alertContainer = document.getElementById('alert-container');
    alertContainer.appendChild(alertBox);

    // Automatically remove the alert after 5 seconds
    setTimeout(() => {
        alertBox.remove();
    }, 5000);
}

// Function to fetch alert data from the server
function fetchAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            data.forEach(alert => {
                generateAlert(alert.type, alert.message);
            });
        })
        .catch(error => console.error('Error fetching alerts:', error));
}

// Function to send alert data to the server
function sendAlert(alertType, message) {
    fetch('/api/alerts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type: alertType, message: message }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Alert sent successfully:', data);
    })
    .catch(error => console.error('Error sending alert:', error));
}

// Function to handle user-triggered alerts
function handleUserAlert() {
    const alertType = document.getElementById('alert-type').value;
    const alertMessage = document.getElementById('alert-message').value;
    
    sendAlert(alertType, alertMessage);
    generateAlert(alertType, alertMessage);
}

// Initialize alerts when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchAlerts();
    
    // Attach event listener for user-triggered alerts
    const alertButton = document.getElementById('send-alert-button');
    alertButton.addEventListener('click', handleUserAlert);
});

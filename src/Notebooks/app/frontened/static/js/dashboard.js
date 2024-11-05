// dashboard.js

// Function to update the dashboard with new data
function updateDashboard(data) {
    // Update key metrics
    document.getElementById('total-incidents').innerText = data.totalIncidents;
    document.getElementById('active-alerts').innerText = data.activeAlerts;
    document.getElementById('evacuations').innerText = data.evacuationCount;

    // Update charts (assuming you have charts for different data points)
    updateIncidentChart(data.incidentTrends);
    updateAlertChart(data.alertDistribution);
    updateEvacuationChart(data.evacuationTrends);
}

// Function to fetch dashboard data from the server
function fetchDashboardData() {
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
}

// Function to initialize charts (this is just a placeholder, you would replace it with actual chart code)
function initializeCharts() {
    // Assuming you're using a charting library like Chart.js
    // Example:
    const ctx = document.getElementById('incidentChart').getContext('2d');
    const incidentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Labels for the chart (e.g., dates)
            datasets: [{
                label: 'Incidents Over Time',
                data: [], // Data points for the chart
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Repeat for other charts (alertChart, evacuationChart, etc.)
}

// Function to update the incident chart with new data
function updateIncidentChart(data) {
    const chart = getChart('incidentChart');
    chart.data.labels = data.labels; // Update labels
    chart.data.datasets[0].data = data.values; // Update data points
    chart.update(); // Refresh the chart
}

// Function to get a chart instance by ID
function getChart(chartId) {
    return Chart.getChart(chartId); // Assuming you're using Chart.js
}

// Event listener to refresh dashboard data periodically
setInterval(fetchDashboardData, 60000); // Refresh data eve

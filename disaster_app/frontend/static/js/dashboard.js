// dashboard.js
// Function to update dashboard data
function updateDashboard(data) {
    // Update various dashboard elements with data
    document.getElementById('totalAlerts').textContent = data.totalAlerts;
    document.getElementById('activeAlerts').textContent = data.activeAlerts;
    document.getElementById('resolvedAlerts').textContent = data.resolvedAlerts;
    document.getElementById('riskLevel').textContent = data.riskLevel;
}

// Function to fetch dashboard data
async function fetchDashboardData() {
    const response = await fetch('/dashboard/data'); // API endpoint to fetch dashboard data
    if (response.ok) {
        const data = await response.json();
        updateDashboard(data); // Update dashboard with fetched data
    } else {
        console.error('Failed to fetch dashboard data:', response.status);
    }
}

// Event listener for page load
document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData(); // Fetch dashboard data when the page loads
});

// Optional: Set an interval to refresh dashboard data periodically
setInterval(fetchDashboardData, 300000); // Refresh every 5 minutes

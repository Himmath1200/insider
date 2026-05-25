/* 
   Insider Threat Detection System - Charts Configuration
   Initializes and manages Chart.js visualizations
*/

/**
 * Initialize Activity Status Pie Chart
 */
function initActivityStatusChart(ctx, suspiciousCount, normalCount) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Suspicious', 'Normal'],
            datasets: [{
                data: [suspiciousCount, normalCount],
                backgroundColor: ['#ff9999', '#66b3ff'],
                borderColor: ['#fff', '#fff'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12, weight: 'bold' }
                    }
                }
            }
        }
    });
}

/**
 * Initialize Alert Severity Chart
 */
function initSeverityChart(ctx, criticalCount, highCount, mediumCount, lowCount) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                label: 'Number of Alerts',
                data: [criticalCount, highCount, mediumCount, lowCount],
                backgroundColor: ['#dc3545', '#fd7e14', '#ffc107', '#28a745'],
                borderRadius: 5,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { font: { size: 11 } }
                },
                y: {
                    ticks: { font: { size: 11, weight: 'bold' } }
                }
            }
        }
    });
}

/**
 * Initialize Role Distribution Chart
 */
function initRoleChart(ctx, roleData) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(roleData),
            datasets: [{
                data: Object.values(roleData),
                backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { size: 12, weight: 'bold' }
                    }
                }
            }
        }
    });
}

/**
 * Initialize Activity Timeline Chart
 */
function initActivityTimelineChart(ctx, dateLabels, activityData) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: dateLabels,
            datasets: [{
                label: 'Activities',
                data: activityData,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { font: { size: 12, weight: 'bold' } }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { font: { size: 11 } }
                },
                x: {
                    ticks: { font: { size: 11 } }
                }
            }
        }
    });
}

/**
 * Initialize Risk Level Distribution Chart
 */
function initRiskLevelChart(ctx, criticalCount, highCount, mediumCount, lowCount) {
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                label: 'Risk Distribution',
                data: [criticalCount, highCount, mediumCount, lowCount],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { font: { size: 12, weight: 'bold' } }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: { font: { size: 10 } }
                }
            }
        }
    });
}

/**
 * Initialize Escalation Type Chart
 */
function initEscalationTypeChart(ctx, typeData) {
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
    
    return new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: Object.keys(typeData),
            datasets: [{
                label: 'Escalation Attempts',
                data: Object.values(typeData),
                backgroundColor: colors,
                borderRadius: 5,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { font: { size: 11 } }
                },
                y: {
                    ticks: { font: { size: 11, weight: 'bold' } }
                }
            }
        }
    });
}

/**
 * Initialize Activity Type Distribution Chart
 */
function initActivityTypeChart(ctx, typeData) {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'];
    
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(typeData),
            datasets: [{
                data: Object.values(typeData),
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12, weight: 'bold' },
                        padding: 15
                    }
                }
            }
        }
    });
}

/**
 * Fetch and display dashboard chart data
 */
async function loadDashboardCharts() {
    try {
        const response = await fetch('/api/dashboard-stats');
        const data = await response.json();
        
        if (data) {
            // Initialize charts with API data
            console.log('Dashboard stats loaded:', data);
        }
    } catch (error) {
        console.error('Error loading dashboard charts:', error);
    }
}

/**
 * Fetch and display escalation chart data
 */
async function loadEscalationCharts() {
    try {
        const response = await fetch('/escalation/api/escalation-stats');
        const data = await response.json();
        
        if (data) {
            console.log('Escalation stats loaded:', data);
        }
    } catch (error) {
        console.error('Error loading escalation charts:', error);
    }
}

/**
 * Fetch and display exfiltration chart data
 */
async function loadExfiltrationCharts() {
    try {
        const response = await fetch('/exfiltration/api/exfiltration-stats');
        const data = await response.json();
        
        if (data) {
            console.log('Exfiltration stats loaded:', data);
        }
    } catch (error) {
        console.error('Error loading exfiltration charts:', error);
    }
}

/**
 * Initialize all charts on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    // Auto-load charts if containers exist
    if (document.getElementById('activityStatusChart')) {
        loadDashboardCharts();
    }
    
    if (document.getElementById('escalationChart')) {
        loadEscalationCharts();
    }
    
    if (document.getElementById('exfiltrationChart')) {
        loadExfiltrationCharts();
    }
});

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initActivityStatusChart,
        initSeverityChart,
        initRoleChart,
        initActivityTimelineChart,
        initRiskLevelChart,
        initEscalationTypeChart,
        initActivityTypeChart,
        loadDashboardCharts,
        loadEscalationCharts,
        loadExfiltrationCharts
    };
}

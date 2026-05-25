/* 
   Insider Threat Detection System - Main JavaScript File
   Handles client-side functionality and interactivity
*/

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Insider Threat Detection System - Loaded');
    
    // Initialize tooltips if any
    initializeTooltips();
    
    // Add auto-dismiss for alerts
    initializeAlerts();
    
    // Add form validation
    initializeFormValidation();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(function(element) {
        new bootstrap.Tooltip(element);
    });
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Format timestamp to readable date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    element.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>';
}

/**
 * Hide loading spinner
 */
function hideLoading(element) {
    element.innerHTML = '';
}

/**
 * Fetch data from API endpoint
 */
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.createElement('div');
    container.innerHTML = toastHtml;
    document.body.insertBefore(container.firstChild, document.body.firstChild);
    
    const alert = document.querySelector('.alert');
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 4000);
}

/**
 * Confirm action before proceeding
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Toggle between two display states
 */
function toggleDisplay(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

/**
 * Search in table
 */
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    const filter = input.value.toUpperCase();
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const text = rows[i].textContent || rows[i].innerText;
        rows[i].style.display = text.toUpperCase().indexOf(filter) > -1 ? '' : 'none';
    }
}

/**
 * Export table to CSV
 */
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(col => {
            rowData.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(rowData.join(','));
    });
    
    // Create download link
    const csvContent = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv.join('\n'));
    const link = document.createElement('a');
    link.setAttribute('href', csvContent);
    link.setAttribute('download', filename || 'export.csv');
    link.click();
}

/**
 * Print document
 */
function printDocument() {
    window.print();
}

/**
 * Filter table rows
 */
function filterTable(selectId, columnIndex, tableId) {
    const select = document.getElementById(selectId);
    const table = document.getElementById(tableId);
    
    if (!select || !table) return;
    
    const filter = select.value.toUpperCase();
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const cell = rows[i].getElementsByTagName('td')[columnIndex];
        if (cell) {
            const text = cell.textContent || cell.innerText;
            rows[i].style.display = filter === '' || text.toUpperCase().includes(filter) ? '' : 'none';
        }
    }
}

/**
 * Clear all form fields
 */
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

/**
 * Disable/Enable button
 */
function toggleButton(buttonId, disabled) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = disabled;
        button.style.opacity = disabled ? '0.5' : '1';
    }
}

/**
 * Get current time in HH:MM:SS format
 */
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString();
}

/**
 * Count down timer
 */
function startCountdown(seconds, callbackFunction) {
    let remaining = seconds;
    
    const interval = setInterval(() => {
        remaining--;
        
        if (remaining <= 0) {
            clearInterval(interval);
            if (typeof callbackFunction === 'function') {
                callbackFunction();
            }
        }
    }, 1000);
}

/**
 * Validate email format
 */
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate password strength
 */
function validatePasswordStrength(password) {
    if (password.length < 12) return 'weak';
    if (!/[A-Z]/.test(password)) return 'weak';
    if (!/[a-z]/.test(password)) return 'weak';
    if (!/[0-9]/.test(password)) return 'weak';
    if (!/[!@#$%^&*]/.test(password)) return 'medium';
    return 'strong';
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'danger');
    });
}

/**
 * Debounce function for search/filter operations
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format number with thousands separator
 */
function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

/**
 * Generate random color
 */
function getRandomColor() {
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#6C5CE7'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchData,
        showToast,
        formatDate,
        showLoading,
        hideLoading,
        exportTableToCSV,
        filterTable,
        searchTable,
        validateEmail,
        validatePasswordStrength
    };
}

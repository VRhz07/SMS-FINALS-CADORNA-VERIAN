// Student Management System - Main JavaScript File

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme based on localStorage
    initializeTheme();
    // Add active class to current navigation item based on URL
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentLocation === linkPath || 
            (linkPath !== '/' && currentLocation.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Flash messages auto-dismiss
    const alertList = document.querySelectorAll('.alert-dismissible');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Auto close after 5 seconds
    });
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            toggleTheme();
        });
    }
});

// Theme functions
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        enableDarkMode();
    } else {
        enableLightMode();
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    if (currentTheme === 'dark') {
        enableLightMode();
    } else {
        enableDarkMode();
    }
}

function enableDarkMode() {
    document.documentElement.setAttribute('data-bs-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    document.getElementById('dark-icon').classList.add('d-none');
    document.getElementById('light-icon').classList.remove('d-none');
}

function enableLightMode() {
    document.documentElement.setAttribute('data-bs-theme', 'light');
    localStorage.setItem('theme', 'light');
    document.getElementById('dark-icon').classList.remove('d-none');
    document.getElementById('light-icon').classList.add('d-none');
}

// Grade calculation helpers
function calculatePercentage(score, maxScore) {
    if (maxScore <= 0) return 0;
    return (score / maxScore) * 100;
}

function getGradeColor(percentage) {
    if (percentage >= 90) return 'success';
    if (percentage >= 80) return 'info';
    if (percentage >= 70) return 'primary';
    if (percentage >= 60) return 'warning';
    return 'danger';
}

// Format date helper
function formatDate(dateStr) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateStr).toLocaleDateString(undefined, options);
}

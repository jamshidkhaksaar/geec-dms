// GEEC Online DMS - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('GEEC DMS loaded successfully');
    initializeApp();
});

function initializeApp() {
    // Check if we're on login page (no sidebar)
    const isLoginPage = !document.querySelector('#sidebar');
    
    // Initialize basic components for all pages
    initializeTooltips();
    initializePopovers();
    initializeFormValidation();
    
    // Only initialize advanced features for authenticated pages
    if (!isLoginPage) {
        initializeAnimations();
        initializeDateTimeUpdates();
        initializeKeyboardShortcuts();
        initializeThemeToggle();
        initializeNotifications();
        
        // Add loading states
        addLoadingStates();
        
        // Initialize specific page components
        if (window.location.pathname.includes('dashboard')) {
            initializeDashboard();
        }
        
        if (window.location.pathname.includes('create_letter')) {
            initializeFileUpload();
        }
        
        if (window.location.pathname.includes('letter_status')) {
            initializeLetterStatus();
        }
    }
}

// Animation Utilities
function initializeAnimations() {
    // Animate cards on page load
    const cards = document.querySelectorAll('.card');
    if (cards && cards.length > 0) {
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    // Animate alerts
    const alerts = document.querySelectorAll('.alert');
    if (alerts && alerts.length > 0) {
        alerts.forEach((alert, index) => {
            alert.classList.add('slide-up');
            
            // Auto-dismiss success alerts after 5 seconds
            if (alert.classList.contains('alert-success')) {
                setTimeout(() => {
                    dismissAlert(alert);
                }, 5000);
            }
        });
    }
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    if (buttons && buttons.length > 0) {
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
}

// Bootstrap component initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Date and time updates
function initializeDateTimeUpdates() {
    updateRelativeTimes();
    setInterval(updateRelativeTimes, 60000); // Update every minute
}

function updateRelativeTimes() {
    const timeElements = document.querySelectorAll('[data-time]');
    timeElements.forEach(element => {
        const timestamp = new Date(element.dataset.time);
        element.textContent = getRelativeTime(timestamp);
    });
}

function getRelativeTime(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days > 1 ? 's' : ''} ago`;
    }
}

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                showFormErrors(form);
            } else {
                showLoadingState(form);
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    field.classList.toggle('is-valid', isValid);
    field.classList.toggle('is-invalid', !isValid);
    
    // Show/hide custom error messages
    const errorElement = field.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.style.display = isValid ? 'none' : 'block';
    }
}

function showFormErrors(form) {
    const firstInvalidField = form.querySelector('.is-invalid, :invalid');
    if (firstInvalidField) {
        firstInvalidField.focus();
        
        // Scroll to the field if it's not visible
        firstInvalidField.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

function showLoadingState(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        const originalText = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        
        // Store original text for potential reset
        submitButton.dataset.originalText = originalText;
    }
}

// Keyboard shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#searchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
}

// Theme toggle (if implemented)
function initializeThemeToggle() {
    const themeToggle = document.querySelector('#themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            toggleTheme();
        });
        
        // Apply saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            applyTheme(savedTheme);
        }
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const themeToggle = document.querySelector('#themeToggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon';
        }
    }
}

// Notification system
function initializeNotifications() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Dashboard specific functions
function initializeDashboard() {
    // Refresh dashboard data periodically
    setInterval(refreshDashboardStats, 300000); // Every 5 minutes
    
    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        // Charts are initialized in the dashboard template
        // This is for any additional chart configurations
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#495057';
    }
}

function refreshDashboardStats() {
    fetch('/api/dashboard-stats', {
        headers: {
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
    })
        .then(response => response.json())
        .then(data => {
            updateStatsCards(data);
        })
        .catch(error => {
            console.error('Error refreshing dashboard stats:', error);
        });
}

function updateStatsCards(stats) {
    const statsElements = {
        verified: document.querySelector('[data-stat="verified"]'),
        pending: document.querySelector('[data-stat="pending"]'),
        rejected: document.querySelector('[data-stat="rejected"]')
    };
    
    Object.keys(statsElements).forEach(key => {
        const element = statsElements[key];
        if (element && stats[key] !== undefined) {
            animateNumber(element, parseInt(element.textContent), stats[key]);
        }
    });
}

function animateNumber(element, from, to) {
    const duration = 1000;
    const start = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(from + (to - from) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// File upload specific functions
function initializeFileUpload() {
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (dropZone && fileInput) {
        // Drag and drop functionality is handled in the template
        // This adds progress tracking for large files
        
        const form = fileInput.closest('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (fileInput.files.length > 0) {
                    showUploadProgress();
                }
            });
        }
    }
}

function showUploadProgress() {
    const progressModal = document.createElement('div');
    progressModal.className = 'modal fade';
    progressModal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Uploading Letter</h5>
                </div>
                <div class="modal-body text-center">
                    <div class="spinner-border text-primary mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>Please wait while your letter is being uploaded...</p>
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(progressModal);
    const modal = new bootstrap.Modal(progressModal);
    modal.show();
}

// Letter status specific functions
function initializeLetterStatus() {
    // Initialize data tables if available
    const table = document.querySelector('#lettersTable');
    if (table && typeof DataTable !== 'undefined') {
        new DataTable(table, {
            responsive: true,
            pageLength: 25,
            order: [[3, 'desc']], // Sort by upload date
            columnDefs: [
                { orderable: false, targets: -1 } // Disable sorting for actions column
            ]
        });
    }
    
    // Auto-refresh letter status
    setInterval(refreshLetterStatus, 30000); // Every 30 seconds
}

function refreshLetterStatus() {
    const statusElements = document.querySelectorAll('[data-letter-status]');
    if (statusElements.length === 0) return;
    
    const letterNumbers = Array.from(statusElements).map(el => el.dataset.letterNumber);
    
    fetch('/api/letter-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
        body: JSON.stringify({ letter_numbers: letterNumbers })
    })
    .then(response => response.json())
    .then(data => {
        updateLetterStatuses(data);
    })
    .catch(error => {
        console.error('Error refreshing letter status:', error);
    });
}

function updateLetterStatuses(updates) {
    updates.forEach(update => {
        const statusElement = document.querySelector(`[data-letter-number="${update.letter_number}"]`);
        if (statusElement && statusElement.dataset.letterStatus !== update.status) {
            // Status has changed, update the UI
            updateLetterStatusElement(statusElement, update);
            
            // Show notification for status change
            showToast(`Letter ${update.letter_number} status updated: ${update.status}`, 'info');
        }
    });
}

function updateLetterStatusElement(element, update) {
    element.dataset.letterStatus = update.status;
    
    const badge = element.querySelector('.badge');
    if (badge) {
        badge.className = `badge bg-${getStatusColor(update.status)}`;
        badge.innerHTML = `<i class="bi bi-${getStatusIcon(update.status)}"></i> ${update.status}`;
    }
    
    // Add animation to highlight the change
    element.classList.add('table-warning');
    setTimeout(() => {
        element.classList.remove('table-warning');
    }, 3000);
}

function getStatusColor(status) {
    switch (status) {
        case 'Verified': return 'success';
        case 'Pending': return 'warning';
        case 'Rejected': return 'danger';
        default: return 'secondary';
    }
}

function getStatusIcon(status) {
    switch (status) {
        case 'Verified': return 'check-circle';
        case 'Pending': return 'clock';
        case 'Rejected': return 'x-circle';
        default: return 'question-circle';
    }
}

// Utility functions
function dismissAlert(alert) {
    alert.style.opacity = '0';
    alert.style.transform = 'translateX(100%)';
    
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 300);
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Copied to clipboard!', 'success');
    }
}

// Loading states utility
function addLoadingStates() {
    const links = document.querySelectorAll('a[href]:not([href^="#"]):not([target="_blank"])');
    links.forEach(link => {
        link.addEventListener('click', function() {
            if (!this.classList.contains('btn-outline-secondary')) {
                this.style.opacity = '0.7';
                this.style.pointerEvents = 'none';
            }
        });
    });
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Only show toast if showToast function exists and we're not on login page
    if (typeof showToast === 'function' && document.querySelector('#sidebar')) {
        showToast('An error occurred. Please refresh the page.', 'danger');
    }
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData && perfData.loadEventEnd - perfData.fetchStart > 3000) {
                console.warn('Page load time is slow:', perfData.loadEventEnd - perfData.fetchStart + 'ms');
            }
        }, 0);
    });
}

// Expose utilities globally
window.GEEC = {
    showToast,
    copyToClipboard,
    dismissAlert,
    showLoadingState,
    animateNumber
}; 
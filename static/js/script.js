// ==================== 
// GLOBAL FUNCTIONS
// ==================== 

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Smooth scroll for anchor links
    initializeSmoothScroll();
    
    // Animate elements on scroll
    initializeScrollAnimations();
}

// ==================== 
// TOOLTIPS
// ==================== 

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ==================== 
// SMOOTH SCROLL
// ==================== 

function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ==================== 
// SCROLL ANIMATIONS
// ==================== 

function initializeScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in', 'slide-up');
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observe all elements with animation classes
    document.querySelectorAll('.stat-card, .feature-card, .step-card').forEach(el => {
        observer.observe(el);
    });
}

// ==================== 
// FORM UTILITIES
// ==================== 

function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.insertBefore(alertDiv, document.body.firstChild);
    
    if (duration > 0) {
        setTimeout(() => {
            alertDiv.remove();
        }, duration);
    }
}

// ==================== 
// API UTILITIES
// ==================== 

async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(endpoint, finalOptions);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// ==================== 
// PREDICTION UTILITIES
// ==================== 

function formatPredictionResult(result) {
    const isPoisonous = result.prediction === 'POISONOUS';
    
    return {
        icon: isPoisonous ? '☠️' : '✅',
        color: isPoisonous ? 'danger' : 'success',
        message: isPoisonous ? 'This mushroom is POISONOUS!' : 'This mushroom is EDIBLE!',
        recommendation: isPoisonous ? 'Do NOT consume this mushroom!' : 'This mushroom appears to be safe to eat.'
    };
}

function updateProgressBar(element, value) {
    element.style.width = value + '%';
    element.textContent = Math.round(value) + '%';
}

// ==================== 
// TABLE UTILITIES
// ==================== 

function populateTable(tableBodyId, data) {
    const tbody = document.getElementById(tableBodyId);
    
    if (!tbody || data.length === 0) {
        return;
    }
    
    tbody.innerHTML = data.map(row => {
        return `<tr>
            ${Object.values(row).map(cell => `<td>${cell}</td>`).join('')}
        </tr>`;
    }).join('');
}

// ==================== 
// STORAGE UTILITIES
// ==================== 

const StorageManager = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Storage Error:', e);
            return false;
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Storage Error:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Storage Error:', e);
            return false;
        }
    },
    
    clear: function() {
        try {
            localStorage.clear();
            return true;
        } catch (e) {
            console.error('Storage Error:', e);
            return false;
        }
    }
};

// ==================== 
// VALIDATION UTILITIES
// ==================== 

function validateForm(formId) {
    const form = document.getElementById(formId);
    
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// ==================== 
// RESPONSIVE UTILITIES
// ==================== 

function isMobile() {
    return window.innerWidth <= 768;
}

function isTablet() {
    return window.innerWidth > 768 && window.innerWidth <= 1024;
}

function isDesktop() {
    return window.innerWidth > 1024;
}

// ==================== 
// FORMATTING UTILITIES
// ==================== 

function formatDate(date) {
    return new Date(date).toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatNumber(number) {
    return new Intl.NumberFormat('id-ID').format(number);
}

function formatPercentage(value, decimals = 2) {
    return (value * 100).toFixed(decimals) + '%';
}

// ==================== 
// EXPORT UTILITIES
// ==================== 

function exportToCSV(data, filename = 'export.csv') {
    const csv = [
        Object.keys(data[0]).join(','),
        ...data.map(row => Object.values(row).join(','))
    ].join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

function exportToJSON(data, filename = 'export.json') {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// ==================== 
// DEBUG UTILITIES
// ==================== 

const Debug = {
    log: function(message, data = null) {
        if (process.env.NODE_ENV === 'development') {
            console.log(`[LOG] ${message}`, data);
        }
    },
    
    warn: function(message, data = null) {
        console.warn(`[WARN] ${message}`, data);
    },
    
    error: function(message, error = null) {
        console.error(`[ERROR] ${message}`, error);
    },
    
    table: function(data) {
        console.table(data);
    }
};

// ==================== 
// NAVIGATION
// ==================== 

function navigateTo(url) {
    window.location.href = url;
}

function goBack() {
    window.history.back();
}

// ==================== 
// MODAL UTILITIES
// ==================== 

function showModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

function hideModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) {
        modal.hide();
    }
}

// ==================== 
// LOADER
// ==================== 

function showLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'flex';
    }
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// ==================== 
// CLIPBOARD
// ==================== 

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success', 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showNotification('Copied to clipboard!', 'success', 2000);
    }
}

// ==================== 
// EXPORT FOR TESTING
// ==================== 

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showNotification,
        apiRequest,
        formatPredictionResult,
        StorageManager,
        validateForm,
        isMobile,
        isTablet,
        isDesktop,
        formatDate,
        formatNumber,
        formatPercentage,
        exportToCSV,
        exportToJSON,
        Debug,
        showLoader,
        hideLoader,
        copyToClipboard
    };
}

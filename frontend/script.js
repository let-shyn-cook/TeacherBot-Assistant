// Chart initialization
const initializeFallsChart = () => {
    const ctx = document.getElementById('fallsChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Falls Detected',
                data: [12, 19, 15, 17, 14, 13],
                borderColor: '#4a90e2',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(74, 144, 226, 0.1)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Falls Detection Trend'
                }
            }
        }
    });
};

// Map initialization
const initializeMap = () => {
    const map = new google.maps.Map(document.getElementById('locationMap'), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8
    });
};

// Alert system
class AlertSystem {
    constructor() {
        this.alertsList = document.querySelector('.alerts-list');
    }

    createAlert(data) {
        const alert = document.createElement('div');
        alert.className = 'alert-item';
        alert.innerHTML = `
            <div class="alert-content">
                <div class="alert-icon ${data.type}">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="alert-details">
                    <h4>${data.title}</h4>
                    <p>${data.description}</p>
                    <span class="alert-time">${data.time}</span>
                </div>
            </div>
            <div class="alert-actions">
                <button class="btn-respond">Respond</button>
                <button class="btn-dismiss">Dismiss</button>
            </div>
        `;
        
        // Add animation
        alert.style.animation = 'fadeIn 0.5s ease';
        
        this.alertsList.prepend(alert);
        
        // Add event listeners
        alert.querySelector('.btn-respond').addEventListener('click', () => this.respondToAlert(data.id));
        alert.querySelector('.btn-dismiss').addEventListener('click', () => this.dismissAlert(alert));
    }

    respondToAlert(id) {
        // Implementation for responding to alert
        console.log(`Responding to alert ${id}`);
    }

    dismissAlert(alertElement) {
        alertElement.style.animation = 'fadeOut 0.5s ease';
        setTimeout(() => alertElement.remove(), 500);
    }
}

// Counter animation
const animateCounters = () => {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.innerText);
        let current = 0;
        const increment = target / 100;
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.innerText = Math.round(current);
                setTimeout(updateCounter, 10);
            } else {
                counter.innerText = target;
            }
        };
        updateCounter();
    });
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeFallsChart();
    initializeMap();
    animateCounters();

    const alertSystem = new AlertSystem();
    
    // Example alert
    setTimeout(() => {
        alertSystem.createAlert({
            id: 1,
            type: 'urgent',
            title: 'Fall Detected',
            description: 'Fall detected in Room 204, Building A',
            time: 'Just now'
        });
    }, 2000);
});

// Responsive sidebar toggle
const toggleSidebar = () => {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
};

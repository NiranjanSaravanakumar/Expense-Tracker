/**
 * ExpenseTracker Chart Initialization
 * Fetches JSON data from /api/chart-data and renders a Chart.js Donut Chart
 */

document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('expensePieChart');

    if (!canvas) {
        return; // Chart canvas not found on this page
    }

    const ctx = canvas.getContext('2d');

    // Premium color palette generated for dark mode
    const chartColors = [
        '#6366f1', // Indigo primary
        '#a855f7', // Purple
        '#ec4899', // Pink
        '#ef4444', // Red
        '#f59e0b', // Amber
        '#10b981', // Emerald
        '#06b6d4', // Cyan
        '#3b82f6', // Blue
        '#8b5cf6', // Violet
        '#f43f5e', // Rose
        '#84cc16', // Lime
        '#64748b'  // Slate (Other)
    ];

    // Fetch data from API endpoint
    fetch('/api/chart-data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Render Chart.js Donut Chart with fetched data
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Total Expenses',
                        data: data.values,
                        backgroundColor: chartColors.slice(0, data.labels.length),
                        borderWidth: 2,
                        borderColor: '#1e293b', // Matches card background
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%', // Makes the donut hole larger (premium look)
                    plugins: {
                        legend: {
                            display: false, // Hidden to save space and look cleaner
                        },
                        tooltip: {
                            backgroundColor: 'rgba(15, 23, 42, 0.9)',
                            titleColor: '#f8fafc',
                            bodyColor: '#cbd5e1',
                            borderColor: '#334155',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: true,
                            boxPadding: 4,
                            usePointStyle: true,
                            callbacks: {
                                label: function (context) {
                                    let label = context.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed !== null) {
                                        label += new Intl.NumberFormat('en-IN', {
                                            style: 'currency',
                                            currency: 'INR'
                                        }).format(context.parsed);
                                    }
                                    return label;
                                }
                            }
                        }
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true,
                        duration: 1500,
                        easing: 'easeOutQuart'
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error loading chart data:", error);
            // Replace canvas area with error message
            canvas.parentElement.innerHTML = `
                <div class="text-center text-danger w-100 h-100 d-flex flex-column align-items-center justify-content-center">
                    <i class="bi bi-exclamation-triangle-fill fs-3 mb-2"></i>
                    <p class="small mb-0">Failed to load chart.</p>
                </div>
            `;
        });
});

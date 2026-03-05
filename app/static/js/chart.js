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

    // Dark Neon Theme colors
    const chartColors = [
        '#FFD500', // Primary Yellow
        '#00FF90', // Income Neon Green
        '#FF6F3C', // Expense Orange
        '#B0B0B0', // Secondary Gray
        '#FFB800', // Amber-Yellow
        '#00E5FF', // Neon Cyan
        '#FF4D8D', // Hot Pink
        '#7B61FF', // Purple
        '#00C9A7', // Teal
        '#FF9A3C', // Light Orange
        '#A8FF3E', // Lime
        '#666666', // Dim Gray (Other)
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

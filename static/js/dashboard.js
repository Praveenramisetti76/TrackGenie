// Set default date to today
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        dateInput.valueAsDate = new Date();
    }

    // Fetch expense data
    fetch('/get_expense_data')
        .then(response => response.json())
        .then(data => {
            // Category Chart
            const categoryCtx = document.getElementById('categoryChart').getContext('2d');
            new Chart(categoryCtx, {
                type: 'pie',
                data: {
                    labels: Object.keys(data.categories),
                    datasets: [{
                        data: Object.values(data.categories),
                        backgroundColor: [
                            '#4CAF50', '#2196F3', '#FFC107', '#F44336', '#9C27B0',
                            '#00BCD4', '#FF9800', '#795548', '#607D8B', '#E91E63',
                            '#3F51B5', '#009688'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });

            // Monthly Comparison Chart
            const monthlyComparisonCtx = document.getElementById('monthlyComparisonChart').getContext('2d');
            const monthlyData = data.monthly;
            const months = Object.keys(monthlyData);
            const expenses = Object.values(monthlyData);

            new Chart(monthlyComparisonCtx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Monthly Expenses',
                        data: expenses,
                        backgroundColor: '#4CAF50',
                        borderColor: '#45a049',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Income vs Expenses Chart
            const incomeExpenseCtx = document.getElementById('incomeExpenseChart').getContext('2d');
            const monthlyIncome = parseFloat(window.monthlyIncomeValue || 0);

            new Chart(incomeExpenseCtx, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [
                        {
                            label: 'Expenses',
                            data: expenses,
                            borderColor: '#4CAF50',
                            backgroundColor: 'rgba(76, 175, 80, 0.1)',
                            fill: true
                        },
                        {
                            label: 'Income',
                            data: Array(months.length).fill(monthlyIncome),
                            borderColor: '#2196F3',
                            backgroundColor: 'rgba(33, 150, 243, 0.1)',
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Update top category
            const categories = data.categories;
            const topCategory = Object.entries(categories).reduce((a, b) => a[1] > b[1] ? a : b)[0];
            document.getElementById('topCategory').textContent = topCategory;

            // Generate expense suggestions
            generateSuggestions(data, monthlyIncome);
        });
});

function generateSuggestions(data, monthlyIncome) {
    const suggestionsDiv = document.getElementById('expenseSuggestions');
    const categories = data.categories;
    const monthlyData = data.monthly;

    // Calculate average monthly spending
    const monthlyValues = Object.values(monthlyData);
    const avgMonthlySpending = monthlyValues.reduce((a, b) => a + b, 0) / monthlyValues.length;

    // Generate suggestions based on spending patterns
    let suggestions = [];

    // Check for high spending categories
    Object.entries(categories).forEach(([category, amount]) => {
        if (amount > avgMonthlySpending * 0.3) {
            suggestions.push({
                type: 'warning',
                message: `Your ${category} expenses are higher than usual. Consider reviewing your spending in this category.`
            });
        }
    });

    // Check for spending trends
    const recentMonths = Object.entries(monthlyData).slice(-3);
    if (recentMonths.length >= 2) {
        const trend = recentMonths[recentMonths.length - 1][1] - recentMonths[recentMonths.length - 2][1];
        if (trend > avgMonthlySpending * 0.2) {
            suggestions.push({
                type: 'info',
                message: 'Your monthly expenses are increasing. Consider setting a budget to control your spending.'
            });
        }
    }

    // Check income vs expenses
    if (avgMonthlySpending > monthlyIncome * 0.8) {
        suggestions.push({
            type: 'warning',
            message: 'Your expenses are close to your income. Consider reducing non-essential spending.'
        });
    }

    // Add general suggestions
    suggestions.push({
        type: 'success',
        message: 'Consider setting up a monthly budget to better track your expenses.'
    });

    // Display suggestions
    suggestions.forEach(suggestion => {
        const suggestionElement = document.createElement('div');
        suggestionElement.className = `expense-suggestion bg-${suggestion.type}`;
        suggestionElement.innerHTML = `
            <i class="fas fa-${suggestion.type === 'warning' ? 'exclamation-triangle' : 
                             suggestion.type === 'info' ? 'info-circle' : 'check-circle'}"></i>
            ${suggestion.message}
        `;
        suggestionsDiv.appendChild(suggestionElement);
    });
} 
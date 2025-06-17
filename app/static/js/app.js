document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});

async function loadDashboard() {
    try {
        // Load summary stats
        const summary = await api.getSummary();
        document.getElementById('total-expenses').textContent = summary.data.total_expenses;
        document.getElementById('total-people').textContent = summary.data.people_count;
        document.getElementById('pending-settlements').textContent = summary.data.settlement_count;
        
        document.getElementById('stats-loading').style.display = 'none';
        document.getElementById('stats-content').style.display = 'block';

        // Load balances
        await loadBalances();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Failed to load dashboard data');
    }
}

async function loadBalances() {
    try {
        const balances = await api.getBalances();
        const balancesContent = document.getElementById('balances-content');
        
        let html = '<div class="row">';
        
        Object.entries(balances.data).forEach(([person, balance]) => {
            const statusClass = balance.status === 'owed' ? 'success' : 
                               balance.status === 'owes' ? 'danger' : 'secondary';
            const statusIcon = balance.status === 'owed' ? '💚' : 
                              balance.status === 'owes' ? '💸' : '✅';
            
            html += `
                <div class="col-md-4 mb-3">
                    <div class="card border-${statusClass}">
                        <div class="card-body">
                            <h6 class="card-title">${statusIcon} ${person}</h6>
                            <p class="mb-1">Paid: ₹${balance.total_paid}</p>
                            <p class="mb-1">Owes: ₹${balance.total_owed}</p>
                            <p class="mb-0"><strong>Net: ₹${balance.net_balance}</strong></p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        balancesContent.innerHTML = html;
        
        document.getElementById('balances-loading').style.display = 'none';
        
    } catch (error) {
        console.error('Error loading balances:', error);
        document.getElementById('balances-content').innerHTML = 
            '<div class="alert alert-danger">Failed to load balances</div>';
        document.getElementById('balances-loading').style.display = 'none';
    }
}

function showAddExpenseModal() {
    const modal = new bootstrap.Modal(document.getElementById('addExpenseModal'));
    modal.show();
}

async function addExpense() {
    const form = document.getElementById('addExpenseForm');
    const formData = new FormData(form);
    
    const expense = {
        amount: parseFloat(document.getElementById('amount').value),
        description: document.getElementById('description').value,
        paid_by: document.getElementById('paid_by').value
    };

    try {
        await api.addExpense(expense);
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addExpenseModal'));
        modal.hide();
        
        // Reset form
        form.reset();
        
        // Reload dashboard
        await loadDashboard();
        
        showSuccess('Expense added successfully!');
        
    } catch (error) {
        console.error('Error adding expense:', error);
        showError('Failed to add expense: ' + error.message);
    }
}
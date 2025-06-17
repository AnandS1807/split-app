let allExpenses = [];
let allPeople = [];
let allSettlements = [];
let currentBalances = {};

document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    loadExpenses();
    loadPeople();
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

async function loadExpenses() {
    try {
        const response = await api.getExpenses();
        allExpenses = response.data;
        displayExpenses(allExpenses);
        
        document.getElementById('expenses-loading').style.display = 'none';
        document.getElementById('expenses-content').style.display = 'block';
        
    } catch (error) {
        console.error('Error loading expenses:', error);
        document.getElementById('expenses-loading').style.display = 'none';
        document.getElementById('expenses-content').innerHTML = 
            '<div class="alert alert-danger">Failed to load expenses</div>';
    }
}

async function loadPeople() {
    try {
        const response = await api.getPeople();
        allPeople = response.data;
        populatePeopleDropdowns();
        populateFilterDropdown();
        
    } catch (error) {
        console.error('Error loading people:', error);
    }
}

async function loadBalances() {
    try {
        const balances = await api.getBalances();
        currentBalances = balances.data;
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

function displayExpenses(expenses) {
    const tbody = document.getElementById('expenses-table-body');
    const noExpenses = document.getElementById('no-expenses');
    
    if (expenses.length === 0) {
        tbody.innerHTML = '';
        noExpenses.style.display = 'block';
        return;
    }
    
    noExpenses.style.display = 'none';
    
    tbody.innerHTML = expenses.map(expense => `
        <tr>
            <td>${formatDate(expense.date)}</td>
            <td>${expense.description}</td>
            <td>₹${expense.amount}</td>
            <td>${expense.paid_by}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary me-1" onclick="editExpense(${expense.id})">
                    ✏️ Edit
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteExpense(${expense.id})">
                    🗑️ Delete
                </button>
            </td>
        </tr>
    `).join('');
}

function populatePeopleDropdowns() {
    const paidBySelect = document.getElementById('paid_by');
    const editPaidBySelect = document.getElementById('editPaidBy');
    
    const options = allPeople.map(person => 
        `<option value="${person.name}">${person.name}</option>`
    ).join('');
    
    paidBySelect.innerHTML = '<option value="">Select person...</option>' + options;
    editPaidBySelect.innerHTML = options;
}

function populateFilterDropdown() {
    const filterSelect = document.getElementById('filterPerson');
    const options = allPeople.map(person => 
        `<option value="${person.name}">${person.name}</option>`
    ).join('');
    
    filterSelect.innerHTML = '<option value="">All People</option>' + options;
}

function filterExpenses() {
    const personFilter = document.getElementById('filterPerson').value;
    const dateFilter = document.getElementById('filterDate').value;
    const searchFilter = document.getElementById('searchDescription').value.toLowerCase();
    
    let filtered = allExpenses;
    
    if (personFilter) {
        filtered = filtered.filter(expense => expense.paid_by === personFilter);
    }
    
    if (dateFilter) {
        filtered = filtered.filter(expense => 
            expense.date.startsWith(dateFilter)
        );
    }
    
    if (searchFilter) {
        filtered = filtered.filter(expense => 
            expense.description.toLowerCase().includes(searchFilter)
        );
    }
    
    displayExpenses(filtered);
}

function clearFilters() {
    document.getElementById('filterPerson').value = '';
    document.getElementById('filterDate').value = '';
    document.getElementById('searchDescription').value = '';
    displayExpenses(allExpenses);
}

function showAddPersonModal() {
    const modal = new bootstrap.Modal(document.getElementById('addPersonModal'));
    modal.show();
}

async function addPerson() {
    const form = document.getElementById('addPersonForm');
    const name = document.getElementById('personName').value.trim();
    
    if (!name) {
        showError('Please enter a name');
        return;
    }
    
    try {
        await api.request('/people', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('addPersonModal'));
        modal.hide();
        form.reset();
        
        // Reload people
        await loadPeople();
        
        showSuccess(`${name} added to the group successfully!`);
        
    } catch (error) {
        console.error('Error adding person:', error);
        showError('Failed to add person: ' + error.message);
    }
}

function showAddExpenseModal() {
    const modal = new bootstrap.Modal(document.getElementById('addExpenseModal'));
    modal.show();
}

async function addExpense() {
    const form = document.getElementById('addExpenseForm');
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

function editExpense(id) {
    const expense = allExpenses.find(e => e.id === id);
    if (!expense) return;
    
    document.getElementById('editExpenseId').value = expense.id;
    document.getElementById('editAmount').value = expense.amount;
    document.getElementById('editDescription').value = expense.description;
    document.getElementById('editPaidBy').value = expense.paid_by;
    
    const modal = new bootstrap.Modal(document.getElementById('editExpenseModal'));
    modal.show();
}

async function updateExpense() {
    const id = document.getElementById('editExpenseId').value;
    const expense = {
        amount: parseFloat(document.getElementById('editAmount').value),
        description: document.getElementById('editDescription').value,
        paid_by: document.getElementById('editPaidBy').value
    };

    try {
        await api.updateExpense(id, expense);
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editExpenseModal'));
        modal.hide();
        
        // Reload expenses
        await loadExpenses();
        
        showSuccess('Expense updated successfully!');
        
    } catch (error) {
        console.error('Error updating expense:', error);
        showError('Failed to update expense: ' + error.message);
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }

    try {
        await api.deleteExpense(id);
        await loadExpenses();
        showSuccess('Expense deleted successfully!');
        
    } catch (error) {
        console.error('Error deleting expense:', error);
        showError('Failed to delete expense: ' + error.message);
    }
}

// ============ SETTLEMENT FUNCTIONS ============

async function calculateOptimalSettlements() {
    const recommendationsContent = document.getElementById('recommendations-content');
    const recommendationsLoading = document.getElementById('recommendations-loading');
    
    recommendationsLoading.style.display = 'block';
    
    try {
        // Calculate optimal settlements based on current balances
        const settlements = calculateMinimumSettlements();
        
        if (settlements.length === 0) {
            recommendationsContent.innerHTML = '<p class="text-success">🎉 All balances are settled!</p>';
        } else {
            let html = '<div class="row">';
            settlements.forEach(settlement => {
                html += `
                    <div class="col-md-6 mb-3">
                        <div class="card border-info">
                            <div class="card-body">
                                <h6 class="card-title">💰 Settlement Needed</h6>
                                <p class="mb-2">
                                    <strong>${settlement.from}</strong> should pay 
                                    <strong>₹${settlement.amount}</strong> to 
                                    <strong>${settlement.to}</strong>
                                </p>
                                <button class="btn btn-sm btn-success" 
                                        onclick="showRecordSettlementModal('${settlement.from}', '${settlement.to}', ${settlement.amount})">
                                    📝 Record Settlement
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            recommendationsContent.innerHTML = html;
        }
        
    } catch (error) {
        console.error('Error calculating settlements:', error);
        recommendationsContent.innerHTML = '<div class="alert alert-danger">Failed to calculate settlements</div>';
    } finally {
        recommendationsLoading.style.display = 'none';
    }
}

function calculateMinimumSettlements() {
    // Simple debt settlement algorithm
    const debts = [];
    const credits = [];
    
    Object.entries(currentBalances).forEach(([person, balance]) => {
        const netBalance = parseFloat(balance.net_balance);
        if (netBalance < 0) {
            debts.push({ person, amount: Math.abs(netBalance) });
        } else if (netBalance > 0) {
            credits.push({ person, amount: netBalance });
        }
    });
    
    const settlements = [];
    let debtIndex = 0;
    let creditIndex = 0;
    
    while (debtIndex < debts.length && creditIndex < credits.length) {
        const debt = debts[debtIndex];
        const credit = credits[creditIndex];
        
        const settlementAmount = Math.min(debt.amount, credit.amount);
        
        settlements.push({
            from: debt.person,
            to: credit.person,
            amount: settlementAmount.toFixed(2)
        });
        
        debt.amount -= settlementAmount;
        credit.amount -= settlementAmount;
        
        if (debt.amount === 0) debtIndex++;
        if (credit.amount === 0) creditIndex++;
    }
    
    return settlements;
}

function showRecordSettlementModal(from, to, amount) {
    document.getElementById('settlementFrom').value = from;
    document.getElementById('settlementTo').value = to;
    document.getElementById('settlementAmount').value = amount;
    document.getElementById('settlementNotes').value = '';
    
    const modal = new bootstrap.Modal(document.getElementById('recordSettlementModal'));
    modal.show();
}

async function recordSettlement() {
    const settlement = {
        from_person: document.getElementById('settlementFrom').value,
        to_person: document.getElementById('settlementTo').value,
        amount: parseFloat(document.getElementById('settlementAmount').value),
        notes: document.getElementById('settlementNotes').value || null,
        status: 'completed'
    };

    try {
        await api.request('/settlements', {
            method: 'POST',
            body: JSON.stringify(settlement)
        });
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('recordSettlementModal'));
        modal.hide();
        
        // Reload data
        await loadDashboard();
        
        showSuccess('Settlement recorded successfully!');
        
    } catch (error) {
        console.error('Error recording settlement:', error);
        showError('Failed to record settlement: ' + error.message);
    }
}
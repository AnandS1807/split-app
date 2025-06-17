class SplitAppAPI {
    constructor() {
        this.baseURL = '/api';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Expense endpoints
    async getExpenses() {
        return this.request('/expenses');
    }

    async addExpense(expense) {
        return this.request('/expenses', {
            method: 'POST',
            body: JSON.stringify(expense)
        });
    }

    async updateExpense(id, expense) {
        return this.request(`/expenses/${id}`, {
            method: 'PUT',
            body: JSON.stringify(expense)
        });
    }

    async deleteExpense(id) {
        return this.request(`/expenses/${id}`, {
            method: 'DELETE'
        });
    }

    // Balance and settlement endpoints
    async getBalances() {
        return this.request('/balances');
    }

    async getSettlements() {
        return this.request('/settlements');
    }

    async getSummary() {
        return this.request('/summary');
    }

    async getPeople() {
        return this.request('/people');
    }
    // Settlement endpoints
    async addSettlement(settlement) {
        return this.request('/settlements', {
            method: 'POST',
            body: JSON.stringify(settlement)
        });
    }

    async updateSettlement(id, updates) {
        return this.request(`/settlements/${id}`, {
            method: 'PUT',
            body: JSON.stringify(updates)
        });
    }
}

// Global API instance
const api = new SplitAppAPI();
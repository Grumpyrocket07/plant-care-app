// API Base URL
const API_URL = 'http://127.0.0.1:8000';

// API Helper Functions
const api = {
    // Auth endpoints
    register: async (name, email, password) => {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                email,
                password,
                language: 'en'
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }
        
        return await response.json();
    },

    login: async (email, password) => {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
        
        return await response.json();
    },

    // Farm endpoints
    getFarms: async (token) => {
        const response = await fetch(`${API_URL}/farms/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch farms');
        }
        
        return await response.json();
    },

    createFarm: async (token, farmData) => {
        const response = await fetch(`${API_URL}/farms/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(farmData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create farm');
        }
        
        return await response.json();
    },

    // Disease detection
    detectDisease: async (token, imageFile, farmId = null) => {
        const formData = new FormData();
        formData.append('file', imageFile);
        if (farmId) {
            formData.append('farm_id', farmId);
        }

        const response = await fetch(`${API_URL}/disease/detect`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Detection failed');
        }
        
        return await response.json();
    },

    getDiseaseHistory: async (token, farmId) => {
        const response = await fetch(`${API_URL}/disease/history/${farmId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch history');
        }
        
        return await response.json();
    }
};

// Token management
const auth = {
    setToken: (token) => {
        localStorage.setItem('token', token);
    },
    
    getToken: () => {
        return localStorage.getItem('token');
    },
    
    removeToken: () => {
        localStorage.removeItem('token');
    },
    
    isLoggedIn: () => {
        return !!localStorage.getItem('token');
    },
    
    logout: () => {
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    }
};
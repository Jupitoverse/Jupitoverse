// static/js/api.js
// Dynamic API URL - works both locally and on network
// When running locally: http://127.0.0.1:5001
// When accessed from network: http://YOUR_MACHINE_IP:5001
const API_BASE_URL = window.location.hostname === '' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5001'  // Local file or localhost
    : `http://${window.location.hostname}:5001`;  // Network access

console.log('🌐 API Base URL:', API_BASE_URL);

// A helper function for making API calls
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const data = await response.json();
        if (!response.ok) {
            // If the server returns an error, throw it so it can be caught
            throw new Error(data.error || 'An unknown API error occurred.');
        }
        return data;
    } catch (error) {
        console.error(`API call to ${endpoint} failed:`, error);
        throw error; // Re-throw the error to be handled by the caller
    }
}

// static/js/api.js

// ... (keep the existing fetchAPI and Auth functions)

const API = {



    // --- Authentication ---
    signup: (fullname, email, password) => { /* ... existing code ... */ },
    login: (email, password) => { /* ... existing code ... */ },

    // --- ADD THESE NEW FUNCTIONS for the Workarounds API ---
    getWorkarounds: () => fetchAPI('/api/workarounds/'),
    addWorkaround: (workaroundData) => {
        return fetchAPI('/api/workarounds/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(workaroundData)
        });
    },
    incrementView: (id) => fetchAPI(`/api/workarounds/${id}/view`, { method: 'POST' }),
    incrementLike: (id) => fetchAPI(`/api/workarounds/${id}/like`, { method: 'POST' }),

// Search Engine logic
    getAllSearchData: () => fetchAPI('/api/search/all'),
    filterAllData: (filters) => {
        return fetchAPI('/api/search/filter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
    },

    updateWorkaround: (id, workaroundData) => {
        return fetchAPI(`/api/workarounds/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(workaroundData)
        });
    },
    deleteWorkaround: (id) => {
        return fetchAPI(`/api/workarounds/${id}`, {
            method: 'DELETE'
        });
    },

};



const API_URL = "http://127.0.0.1:8000";

async function apiFetch(endpoint, options = {}) {
    const response = await fetch(`${API_URL}${endpoint}`, {
        headers: { "Content-Type": "application/json" },
        ...options
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error);
    }

    return response.json();
}

import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

// Interceptor to add auth token
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default {
    submitFeedback(data) {
        return api.post('/feedback', data);
    },
    login(credentials) {
        return api.post('/auth/login', credentials);
    },
    getFeedbacks() {
        return api.get('/admin/feedbacks');
    },
    deleteFeedback(id) {
        return api.delete(`/admin/feedbacks/${id}`);
    },
    exportFeedbacks() {
        return api.get('/admin/export', { responseType: 'blob' });
    }
};

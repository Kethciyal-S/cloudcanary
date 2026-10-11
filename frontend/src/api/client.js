import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://cloudcanary.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

export const getEvents = async (limit = 50) => {
  const response = await api.get(`/events?limit=${limit}`);
  return response.data;
};

export const getStats = async () => {
  const response = await api.get('/events/stats');
  return response.data;
};

export default api;

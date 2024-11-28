import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (email, password) => {
  const response = await api.post('/auth/login', { username: email, password });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const getTeams = async (conference) => {
  const response = await api.get('/teams', { params: { conference } });
  return response.data;
};

export const getGames = async (date) => {
  const response = await api.get('/games', { params: { date } });
  return response.data;
};

export const getPlayers = async (teamId) => {
  const response = await api.get('/players', { params: { team_id: teamId } });
  return response.data;
};

export default api; 
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = {
  getEnergyValveData: () => axios.get(`${API_URL}/api/energy-valve-data/`),
  getHourlyHeatmap: () => axios.get(`${API_URL}/api/hourly-heatmap/`),
  // Add more API functions for other visualizations
};
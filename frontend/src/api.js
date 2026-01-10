import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const fetchLatestSnapshot = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/cto/latest`);
        return response.data;
    } catch (error) {
        console.error('Error fetching latest snapshot:', error);
        throw error;
    }
};

export const fetchHistory = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/cto/history`);
        return response.data;
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
};

export const triggerRun = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/cto/run`);
        return response.data;
    } catch (error) {
        console.error('Error triggering run:', error);
        throw error;
    }
};

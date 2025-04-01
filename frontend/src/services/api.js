import axios from 'axios';

const API_URL = 'https://student-dropout-a5to.onrender.com';

export const uploadTrainData = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return await axios.post(`${API_URL}/upload_train_data`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const retrainModel = async () => {
  return await axios.post(`${API_URL}/retrain`);
};

export const makePrediction = async (data) => {
  return await axios.post(`${API_URL}/predict`, data);
};

export const evaluateModel = async () => {
  return await axios.post(`${API_URL}/evaluate`);
};

export const getVisualization = async (featureName) => {
  return await axios.get(`${API_URL}/visualize/${featureName}`);
};
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://localhost:4000';

export const getQuickSightEmbedUrl = async (dashboardId) => {
  console.log("Making request for Dashboard ID:", dashboardId); // Debugging line
  try {
    const response = await axios.post(`${API_BASE_URL}/quicksight-embed-url`, {
      dashboardId,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log("Response from backend:", response.data);
    return response.data.embedUrl;
  } catch (error) {
    console.error('Error fetching QuickSight embed URL:', error); // Detailed error logging
    throw error;
  }
};

export const getSageMakerPredictions = async (inputData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/sagemaker-predict`, {
      inputData,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data.prediction;
  } catch (error) {
    console.error('Error fetching SageMaker predictions:', error);
    throw error;
  }
};

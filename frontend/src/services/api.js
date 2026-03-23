const API_BASE_URL = 'http://127.0.0.1:8000';

export const analyzeNews = async (text, type = 'text') => {
  const payload = {
    text: type === 'text' ? text : null,
    url: type === 'url' ? text : null
  };

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Scanner Anomaly Detected');
    }
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

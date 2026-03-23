const API_BASE_URL = 'http://127.0.0.1:8000';

export const analyzeNews = async (text, type = 'text') => {
  const payload = {
    text: type === 'text' ? text : null,
    url: type === 'url' ? text : null
  };

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
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
export const submitFeedback = async (text, label) => {
  try {
    const response = await fetch(`${API_BASE_URL}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, label })
    });
    return await response.json();
  } catch (error) {
    console.error('Feedback Error:', error);
    throw error;
  }
};
export const generateFake = async (text) => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate_fake`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    return await response.json();
  } catch (error) {
    console.error('Generation Error:', error);
    throw error;
  }
};

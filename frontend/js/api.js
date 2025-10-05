/**
 * API module for communicating with the Token Calculator backend
 */

// API Configuration
const API_CONFIG = {
  baseURL: 'http://localhost:5000',
  endpoints: {
    calculate: '/api/calculate'
  },
  timeout: 30000 // 30 seconds
};

/**
 * Calculate tokens via API
 * @param {string} text - The text to tokenize
 * @param {string} model - The model name
 * @param {boolean} preprocessMarkdown - Whether to preprocess markdown
 * @returns {Promise<Object>} - Result object with token_count, character_count, model
 */
async function calculateTokens(text, model, preprocessMarkdown = true) {
  const url = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.calculate}`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        model: model,
        preprocess_markdown: preprocessMarkdown
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API request failed: ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error('Request timeout. Please try again.');
    }

    if (error.message.includes('Failed to fetch')) {
      throw new Error('Unable to connect to server. Make sure the backend is running.');
    }

    throw error;
  }
}

/**
 * Check if the API is available
 * @returns {Promise<boolean>} - True if API is available
 */
async function checkAPIHealth() {
  try {
    const response = await fetch(`${API_CONFIG.baseURL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(3000)
    });
    return response.ok;
  } catch (error) {
    return false;
  }
}

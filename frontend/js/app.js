/**
 * Main application logic for Token Calculator
 */

// DOM Elements
const textInput = document.getElementById('textInput');
const fileInput = document.getElementById('fileInput');
const charCounter = document.getElementById('charCounter');
const modelSelect = document.getElementById('modelSelect');
const preprocessCheckbox = document.getElementById('preprocessMarkdown');
const calculateBtn = document.getElementById('calculateBtn');
const calculateBtnText = document.getElementById('calculateBtnText');
const clearBtn = document.getElementById('clearBtn');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const tokenCount = document.getElementById('tokenCount');
const charCount = document.getElementById('charCount');
const modelUsed = document.getElementById('modelUsed');
const copyBtn = document.getElementById('copyBtn');
const successMessage = document.getElementById('successMessage');
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

// State
let isCalculating = false;
let lastResult = null;

/**
 * Initialize the application
 */
function init() {
  // Initialize theme
  initializeTheme();
  updateThemeIcon();

  // Add event listeners
  textInput.addEventListener('input', debounce(updateCharacterCount, 300));
  fileInput.addEventListener('change', handleFileUpload);
  calculateBtn.addEventListener('click', handleCalculate);
  clearBtn.addEventListener('click', handleClear);
  copyBtn.addEventListener('click', handleCopy);
  themeToggle.addEventListener('click', toggleTheme);

  // Keyboard shortcuts
  textInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleCalculate();
    }
  });

  // Initial character count
  updateCharacterCount();

  // Check API health on load
  checkAPIHealth().then(isHealthy => {
    if (!isHealthy) {
      showError('Backend server is not running. Please start the API server.');
    }
  });
}

/**
 * Update character counter
 */
function updateCharacterCount() {
  const count = textInput.value.length;
  charCounter.textContent = `${formatNumber(count)} character${count !== 1 ? 's' : ''}`;
}

/**
 * Handle file upload
 */
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const content = await readFileContent(file);
    textInput.value = content;
    updateCharacterCount();
    hideError();
  } catch (error) {
    showError('Failed to read file. Please try again.');
  }

  // Reset file input
  fileInput.value = '';
}

/**
 * Handle calculate button click
 */
async function handleCalculate() {
  const text = textInput.value;
  const model = modelSelect.value;
  const preprocess = preprocessCheckbox.checked;

  // Validate input
  const validation = validateInput(text);
  if (!validation.isValid) {
    showError(validation.error);
    return;
  }

  // Hide previous error/results
  hideError();
  hideResults();

  // Set loading state
  setLoadingState(true);

  try {
    // Call API
    const result = await calculateTokens(text, model, preprocess);

    // Store result
    lastResult = result;

    // Display results
    displayResults(result);

  } catch (error) {
    showError(error.message);
  } finally {
    setLoadingState(false);
  }
}

/**
 * Handle clear button click
 */
function handleClear() {
  textInput.value = '';
  updateCharacterCount();
  hideError();
  hideResults();
  hideSuccess();
  lastResult = null;
}

/**
 * Handle copy button click
 */
async function handleCopy() {
  if (!lastResult) return;

  const copyText = `Token Count: ${formatNumber(lastResult.token_count)}
Model: ${lastResult.model}
Characters: ${formatNumber(lastResult.character_count)}`;

  try {
    await copyToClipboard(copyText);
    showSuccess('Results copied to clipboard!');
  } catch (error) {
    showError('Failed to copy to clipboard.');
  }
}

/**
 * Display results
 */
function displayResults(result) {
  tokenCount.textContent = formatNumber(result.token_count);
  charCount.textContent = formatNumber(result.character_count);
  modelUsed.textContent = result.model;

  resultsSection.classList.remove('hidden');

  // Smooth scroll to results
  resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Hide results
 */
function hideResults() {
  resultsSection.classList.add('hidden');
}

/**
 * Show error message
 */
function showError(message) {
  errorMessage.textContent = message;
  errorMessage.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideError() {
  errorMessage.classList.add('hidden');
  errorMessage.textContent = '';
}

/**
 * Show success message
 */
function showSuccess(message) {
  successMessage.textContent = message;
  showTemporaryMessage(successMessage, 3000);
}

/**
 * Hide success message
 */
function hideSuccess() {
  successMessage.classList.add('hidden');
}

/**
 * Set loading state
 */
function setLoadingState(loading) {
  isCalculating = loading;

  if (loading) {
    calculateBtn.disabled = true;
    calculateBtnText.innerHTML = '<span class="spinner"></span> Calculating...';
  } else {
    calculateBtn.disabled = false;
    calculateBtnText.textContent = 'Calculate';
  }
}

/**
 * Toggle theme
 */
function toggleTheme() {
  const currentTheme = getCurrentTheme();
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  setTheme(newTheme);
  updateThemeIcon();
}

/**
 * Update theme icon
 */
function updateThemeIcon() {
  const theme = getCurrentTheme();
  themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

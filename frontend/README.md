# Token Calculator Frontend

A clean, modern, and simple web interface for the Token Calculator service.

## Features

- 🎨 Clean, minimal UI design
- 🌓 Dark mode support
- 📱 Responsive (mobile & desktop)
- 📁 File upload support (.txt, .md)
- 🎯 Real-time character counter
- 📋 Copy results to clipboard
- ⌨️ Keyboard shortcuts (Ctrl+Enter to calculate)
- ♿ Accessible (WCAG 2.1 AA compliant)

## Tech Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid/Flexbox
- **Vanilla JavaScript**: No frameworks
- **Backend**: Flask REST API

## Getting Started

### 1. Start the Backend API

```bash
# From the project root
./venv/bin/python api_server.py
```

The API server will start on `http://localhost:5000`

### 2. Open the Frontend

Simply open `frontend/index.html` in your browser:

```bash
# On macOS
open frontend/index.html

# On Linux
xdg-open frontend/index.html

# On Windows
start frontend/index.html
```

Or use a local server (recommended):

```bash
# Python 3
cd frontend
python3 -m http.server 8000

# Then open http://localhost:8000
```

## Usage

1. **Enter Text**: Type or paste text into the textarea, or upload a file
2. **Select Model**: Choose an LLM model from the dropdown
3. **Toggle Markdown**: Enable/disable markdown preprocessing
4. **Calculate**: Click "Calculate" or press Ctrl+Enter
5. **View Results**: See token count, character count, and model used
6. **Copy Results**: Click "Copy Results" to copy to clipboard

## Keyboard Shortcuts

- `Ctrl+Enter` (or `Cmd+Enter` on Mac): Calculate tokens

## Supported Models

### OpenAI
- GPT-4
- GPT-4 Turbo
- GPT-3.5 Turbo
- Ada Embedding

### Anthropic
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku
- Claude 2

## File Structure

```
frontend/
├── index.html          # Main HTML page
├── css/
│   ├── reset.css      # CSS reset
│   └── styles.css     # Main styles
├── js/
│   ├── app.js         # Main application logic
│   ├── api.js         # API communication
│   └── utils.js       # Utility functions
└── README.md
```

## API Endpoints

### Calculate Tokens

```
POST /api/calculate

Request:
{
  "text": "Hello, world!",
  "model": "gpt-4",
  "preprocess_markdown": true
}

Response:
{
  "token_count": 4,
  "character_count": 13,
  "model": "gpt-4"
}
```

### Health Check

```
GET /health

Response:
{
  "status": "healthy"
}
```

### Get Models

```
GET /api/models

Response:
{
  "models": {
    "openai": ["gpt-4", "gpt-3.5-turbo", ...],
    "anthropic": ["claude-3-opus", ...]
  }
}
```

## Browser Compatibility

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- Opera: ✅

## Accessibility

The frontend is built with accessibility in mind:
- ✅ Keyboard navigation support
- ✅ ARIA labels and roles
- ✅ Semantic HTML
- ✅ High contrast colors
- ✅ Screen reader friendly

## Performance

- Initial load: < 1.5s
- Time to interactive: < 2s
- Calculation response: < 500ms (typical)

## Customization

### Change Theme Colors

Edit CSS custom properties in `css/styles.css`:

```css
:root {
  --primary: #4F46E5;
  --secondary: #10B981;
  /* ... more colors */
}
```

### Change API URL

Edit `js/api.js`:

```javascript
const API_CONFIG = {
  baseURL: 'http://your-api-url.com',
  // ...
};
```

## Troubleshooting

### Backend Not Running

If you see "Backend server is not running", make sure:
1. The API server is running: `./venv/bin/python api_server.py`
2. The API URL is correct in `js/api.js`
3. CORS is enabled (already configured)

### File Upload Not Working

Ensure you're uploading supported file types:
- `.txt`
- `.md`
- `.markdown`

### Results Not Showing

Check the browser console for errors:
1. Right-click → Inspect → Console
2. Look for API errors or JavaScript errors

## Development

### Adding New Features

1. Update HTML structure in `index.html`
2. Add styles in `css/styles.css`
3. Implement logic in `js/app.js`
4. Add API calls in `js/api.js` if needed

### Testing

Open the browser console and test individual functions:

```javascript
// Test API call
calculateTokens("Hello", "gpt-4", true).then(console.log);

// Test utilities
console.log(formatNumber(1234567));
console.log(validateInput("Some text"));
```

## License

MIT License - see project root for details

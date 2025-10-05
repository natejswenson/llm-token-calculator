# Token Calculator Service

A complete web application for calculating token counts for various LLM models. Features a clean, modern web interface integrated with a Python Flask backend.

## Features

- 🎨 **Modern Web UI**: Clean, responsive interface with dark mode
- 🤖 **Multi-Model Support**: OpenAI (GPT-4, GPT-3.5) and Anthropic (Claude) models
- 📝 **Markdown Processing**: Automatic preprocessing of markdown content
- 📁 **File Upload**: Support for .txt and .md files
- ⚡ **Fast & Responsive**: Real-time character counting and instant results
- 📋 **Copy to Clipboard**: Easy result sharing
- ♿ **Accessible**: WCAG 2.1 AA compliant
- 🌓 **Dark Mode**: Beautiful light and dark themes
- 🔒 **Security Hardened**: CORS protection, security headers, input validation, error sanitization

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd context-tokens

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the integrated web application
./venv/bin/python app.py

# Application will be available at:
# http://localhost:5000
```

Open your browser and navigate to `http://localhost:5000` to use the web interface!

## Project Structure

```
context-tokens/
├── app.py                      # Main Flask application (frontend + API)
├── api_server.py               # Standalone API server (if needed)
├── example.py                  # CLI example script
├── src/                        # Core token calculator library
│   ├── calculator.py          # TokenCalculator class
│   ├── models.py              # Model configurations
│   ├── preprocessor.py        # Markdown preprocessing
│   └── tokenizers/            # Tokenizer implementations
│       ├── base.py
│       ├── openai.py
│       └── anthropic.py
├── templates/                  # Flask HTML templates
│   └── index.html
├── static/                     # Static assets (CSS, JS)
│   ├── css/
│   │   ├── reset.css
│   │   └── styles.css
│   └── js/
│       ├── api.js
│       ├── app.js
│       └── utils.js
├── tests/                      # Test suite (51 tests, 89% coverage)
├── requirements.txt
└── README.md
```

## Usage

### Web Interface

1. **Enter Text**: Type or paste text, or upload a file
2. **Select Model**: Choose from OpenAI or Anthropic models
3. **Configure Options**: Toggle markdown preprocessing
4. **Calculate**: Click "Calculate" or press Ctrl+Enter
5. **View Results**: See token count, character count, and model
6. **Copy Results**: Click to copy results to clipboard

### CLI Usage

```bash
# Calculate tokens from command line
./venv/bin/python example.py --model gpt-4 --input "Hello, world!"

# With file input
./venv/bin/python example.py --model claude-3-opus --input document.md --detailed

# Disable markdown preprocessing
./venv/bin/python example.py --model gpt-4 --input "# Title" --no-preprocess
```

### Python API

```python
from src.calculator import TokenCalculator

# Create calculator
calculator = TokenCalculator()

# Calculate tokens
count = calculator.calculate("Hello, world!", model="gpt-4")
print(f"Tokens: {count}")  # Output: Tokens: 4

# Get detailed information
result = calculator.calculate_detailed("Hello, world!", model="gpt-4")
print(result)
# {'token_count': 4, 'model': 'gpt-4', 'character_count': 13}

# Process markdown
markdown_text = "# Title\n\nThis is **bold** text"
count = calculator.calculate(markdown_text, model="claude-3-opus")
```

## Supported Models

### OpenAI
- `gpt-4` - GPT-4
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5-turbo` - GPT-3.5 Turbo
- `text-embedding-ada-002` - Ada Embedding

### Anthropic
- `claude-3-opus` - Claude 3 Opus
- `claude-3-sonnet` - Claude 3 Sonnet
- `claude-3-haiku` - Claude 3 Haiku
- `claude-2` - Claude 2

## API Endpoints

### Web UI
- `GET /` - Main web interface

### API
- `GET /health` - Health check
- `POST /api/calculate` - Calculate tokens
- `GET /api/models` - List supported models

### Example API Request

```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "model": "gpt-4",
    "preprocess_markdown": true
  }'
```

Response:
```json
{
  "token_count": 4,
  "character_count": 13,
  "model": "gpt-4"
}
```

## Configuration

### Environment Variables

```bash
# Server port (default: 5000)
export PORT=8080

# Debug mode (default: False)
export DEBUG=true

# Anthropic API key (for Claude models with exact tokenization)
# Without this key, Claude models will use approximate tokenization
export ANTHROPIC_API_KEY=your-key-here

# Allowed CORS origins (default: http://localhost:5000)
# Comma-separated list for multiple origins
export ALLOWED_ORIGINS=http://localhost:5000,https://yourdomain.com
```

## Development

### Running Tests

```bash
# Run all tests
./venv/bin/python -m pytest tests/ -v

# Run with coverage
./venv/bin/python -m pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
./venv/bin/python -m pytest tests/test_calculator.py -v
```

### Test Coverage

Current coverage: **89%**

- Core calculator: 97%
- Tokenizers: 76-78%
- Markdown preprocessor: 100%
- 51 passing tests

### Code Quality

```bash
# Format code
./venv/bin/black src/ tests/

# Lint code
./venv/bin/ruff check src/ tests/

# Type checking
./venv/bin/mypy src/
```

## Keyboard Shortcuts

- `Ctrl+Enter` (or `Cmd+Enter` on Mac): Calculate tokens
- Theme toggle button: Switch between light and dark mode

## Browser Compatibility

- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ Opera

## Performance

- Page load: < 1.5s
- Calculation response: < 500ms (typical)
- Supports large inputs (up to 1M characters)

## Security

This application includes multiple security features:

- **CORS Protection**: Configurable allowed origins (default: localhost only)
- **Security Headers**: Content Security Policy, X-Frame-Options, X-XSS-Protection, HSTS
- **Input Validation**: Type checking, size limits (1MB max), model whitelist
- **Error Sanitization**: Sensitive information filtered from error messages
- **No Code Execution**: All processing uses safe regex transformations
- **Client-Side File Reading**: File uploads processed in browser only

### Production Security Checklist

When deploying to production:

1. ✅ Set `ALLOWED_ORIGINS` to your actual domain(s)
2. ✅ Enable HTTPS (required for HSTS header)
3. ✅ Set `DEBUG=false`
4. ✅ Use environment variables for secrets (never hardcode)
5. ✅ Consider adding rate limiting (e.g., Flask-Limiter)
6. ✅ Monitor and rotate API keys regularly
7. ✅ Enable centralized logging
8. ✅ Keep dependencies updated

## Troubleshooting

### Application Won't Start

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Anthropic Models Error

Claude models work without an API key using approximate tokenization. For exact token counts, set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY=your-key-here
```

**Note**: Without an API key, Claude models return approximate token counts using a character-based heuristic (~3.7 chars/token).

### Port Already in Use

Change the port:
```bash
PORT=8080 ./venv/bin/python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Implement your changes
5. Run tests and ensure coverage stays above 90%
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [tiktoken](https://github.com/openai/tiktoken) - OpenAI tokenization
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) - Anthropic SDK
- Flask - Web framework
- Built with ❤️ using TDD principles

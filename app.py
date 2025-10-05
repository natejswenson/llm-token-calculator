#!/usr/bin/env python3
"""Flask application for Token Calculator - integrated frontend and API."""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from src.calculator import TokenCalculator
import os

app = Flask(__name__)

# Configure CORS with restricted origins
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5000').split(',')
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

# Security headers
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self'; connect-src 'self'"
    return response


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/calculate', methods=['POST'])
def calculate_tokens():
    """Calculate tokens for given text and model.

    Request JSON:
        {
            "text": "string",
            "model": "gpt-4",
            "preprocess_markdown": true
        }

    Response JSON:
        {
            "token_count": 123,
            "character_count": 456,
            "model": "gpt-4"
        }
    """
    try:
        # Get request data - handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.get_json(force=True, silent=True)

        if data is None:
            data = request.form.to_dict()

        if not data:
            return jsonify({'error': 'Invalid request: No JSON data provided'}), 400

        # Validate required fields
        if 'text' not in data:
            return jsonify({'error': 'Missing required field: text'}), 400

        if 'model' not in data:
            return jsonify({'error': 'Missing required field: model'}), 400

        text = data['text']
        model = data['model']
        preprocess_markdown = data.get('preprocess_markdown', True)

        # Input validation
        if not isinstance(text, str):
            return jsonify({'error': 'Invalid text field: must be a string'}), 400

        if not isinstance(model, str):
            return jsonify({'error': 'Invalid model field: must be a string'}), 400

        if len(text) > 1000000:  # 1MB text limit
            return jsonify({'error': 'Text too large. Maximum 1,000,000 characters.'}), 400

        # Sanitize model name to prevent potential issues
        allowed_models = [
            'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'text-embedding-ada-002',
            'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', 'claude-2'
        ]
        if model not in allowed_models:
            return jsonify({'error': f'Unsupported model: {model}'}), 400

        # Create calculator with markdown preprocessing setting
        calc = TokenCalculator(preprocess_markdown=preprocess_markdown)

        # Calculate tokens
        result = calc.calculate_detailed(text, model)

        return jsonify(result), 200

    except ValueError as e:
        # Model validation errors
        error_msg = str(e)
        app.logger.warning(f'Validation error: {error_msg}')
        return jsonify({'error': error_msg}), 400

    except Exception as e:
        # Unexpected errors - sanitize error messages
        app.logger.error(f'Unexpected error: {e}', exc_info=True)

        # Never expose sensitive information in errors
        error_msg = str(e)

        # Filter out any potential sensitive data
        sensitive_keywords = ['ANTHROPIC_API_KEY', 'API_KEY', 'SECRET', 'PASSWORD', 'TOKEN']
        for keyword in sensitive_keywords:
            if keyword in error_msg.upper():
                return jsonify({'error': 'Internal server error. Please check server logs.'}), 500

        # Return sanitized error message
        return jsonify({'error': 'An error occurred while processing your request.'}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of supported models.

    Response JSON:
        {
            "models": {
                "openai": [...],
                "anthropic": [...]
            }
        }
    """
    from src.models import SUPPORTED_MODELS

    # Group models by provider
    models_by_provider = {}
    for model, provider in SUPPORTED_MODELS.items():
        if provider not in models_by_provider:
            models_by_provider[provider] = []
        models_by_provider[provider].append(model)

    return jsonify({'models': models_by_provider}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    import os

    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    print(f"""
    ╔════════════════════════════════════════╗
    ║   Token Calculator Web Application     ║
    ╠════════════════════════════════════════╣
    ║   Application running on:              ║
    ║   http://localhost:{port}                 ║
    ║                                        ║
    ║   Open in your browser to use the UI   ║
    ║                                        ║
    ║   API Endpoints:                       ║
    ║   GET  /                               ║
    ║   GET  /health                         ║
    ║   POST /api/calculate                  ║
    ║   GET  /api/models                     ║
    ╚════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)

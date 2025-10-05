#!/usr/bin/env python3
"""Flask API server for Token Calculator frontend."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.calculator import TokenCalculator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize calculator
calculator = TokenCalculator()


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

        # Create calculator with markdown preprocessing setting
        calc = TokenCalculator(preprocess_markdown=preprocess_markdown)

        # Calculate tokens
        result = calc.calculate_detailed(text, model)

        return jsonify(result), 200

    except ValueError as e:
        # Model validation errors
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        # Unexpected errors
        app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'Internal server error'}), 500


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
    ║   Token Calculator API Server          ║
    ╠════════════════════════════════════════╣
    ║   Server running on:                   ║
    ║   http://localhost:{port}                 ║
    ║                                        ║
    ║   Endpoints:                           ║
    ║   GET  /health                         ║
    ║   POST /api/calculate                  ║
    ║   GET  /api/models                     ║
    ╚════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)

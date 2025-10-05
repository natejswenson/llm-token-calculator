"""Model configuration and constants."""

from typing import Dict, Set

# Supported models mapping
SUPPORTED_MODELS: Dict[str, str] = {
    # OpenAI models
    "gpt-4": "openai",
    "gpt-4-turbo": "openai",
    "gpt-3.5-turbo": "openai",
    "text-embedding-ada-002": "openai",
    # Anthropic models
    "claude-3-opus": "anthropic",
    "claude-3-sonnet": "anthropic",
    "claude-3-haiku": "anthropic",
    "claude-2": "anthropic",
}


def get_tokenizer_type(model: str) -> str:
    """Get the tokenizer type for a given model.

    Args:
        model: The model name

    Returns:
        The tokenizer type (e.g., 'openai', 'anthropic')

    Raises:
        ValueError: If the model is not supported
    """
    if model not in SUPPORTED_MODELS:
        raise ValueError(
            f"Unsupported model: {model}. "
            f"Supported models: {', '.join(SUPPORTED_MODELS.keys())}"
        )
    return SUPPORTED_MODELS[model]


def is_supported_model(model: str) -> bool:
    """Check if a model is supported.

    Args:
        model: The model name

    Returns:
        True if the model is supported, False otherwise
    """
    return model in SUPPORTED_MODELS

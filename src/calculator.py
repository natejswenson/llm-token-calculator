"""Main TokenCalculator class."""

from typing import Dict, Optional
from .models import get_tokenizer_type, is_supported_model
from .tokenizers.base import BaseTokenizer
from .preprocessor import MarkdownPreprocessor


class TokenCalculator:
    """Main entry point for token calculation across different LLM models."""

    def __init__(self, preprocess_markdown: bool = True):
        """Initialize the TokenCalculator.

        Args:
            preprocess_markdown: Whether to preprocess markdown before tokenization
        """
        self._tokenizers: Dict[str, BaseTokenizer] = {}
        self._preprocess_markdown = preprocess_markdown
        self._preprocessor = MarkdownPreprocessor() if preprocess_markdown else None

    def calculate(self, text: str, model: str) -> int:
        """Calculate the number of tokens in the given text for the specified model.

        Args:
            text: The text to tokenize
            model: The model name (e.g., 'gpt-4', 'claude-3-opus')

        Returns:
            The number of tokens

        Raises:
            ValueError: If the model is not supported
        """
        # Validate model
        if not is_supported_model(model):
            raise ValueError(
                f"Unsupported model: {model}. "
                f"Use one of: gpt-4, gpt-4-turbo, gpt-3.5-turbo, "
                f"claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-2"
            )

        # Handle empty or whitespace-only text
        if not text or not text.strip():
            return 0

        # Preprocess markdown if enabled
        processed_text = text
        if self._preprocessor:
            processed_text = self._preprocessor.process(text)

        # Get or create tokenizer for this model
        tokenizer_type = get_tokenizer_type(model)
        tokenizer = self._get_tokenizer(model, tokenizer_type)

        # Count tokens
        return tokenizer.count_tokens(processed_text)

    def _get_tokenizer(self, model: str, tokenizer_type: str) -> BaseTokenizer:
        """Get or create a tokenizer instance for the given model.

        Args:
            model: The model name
            tokenizer_type: The tokenizer type ('openai' or 'anthropic')

        Returns:
            A tokenizer instance
        """
        # Return cached tokenizer if available
        if model in self._tokenizers:
            return self._tokenizers[model]

        # Create new tokenizer
        if tokenizer_type == "openai":
            from .tokenizers.openai import OpenAITokenizer

            tokenizer = OpenAITokenizer(model)
        elif tokenizer_type == "anthropic":
            from .tokenizers.anthropic import AnthropicTokenizer

            tokenizer = AnthropicTokenizer(model)
        else:
            raise ValueError(f"Unknown tokenizer type: {tokenizer_type}")

        # Cache and return
        self._tokenizers[model] = tokenizer
        return tokenizer

    def calculate_detailed(
        self, text: str, model: str
    ) -> Dict[str, int | str | bool]:
        """Calculate tokens and return detailed information.

        Args:
            text: The text to tokenize
            model: The model name

        Returns:
            A dictionary with token_count, model, character_count, and is_approximate
        """
        token_count = self.calculate(text, model)

        # Check if using approximation for Anthropic models
        is_approximate = False
        tokenizer_type = get_tokenizer_type(model)
        if tokenizer_type == "anthropic":
            tokenizer = self._get_tokenizer(model, tokenizer_type)
            if hasattr(tokenizer, 'is_using_approximation'):
                is_approximate = tokenizer.is_using_approximation()

        result = {
            "token_count": token_count,
            "model": model,
            "character_count": len(text),
        }

        # Add approximation flag if applicable
        if is_approximate:
            result["is_approximate"] = True

        return result

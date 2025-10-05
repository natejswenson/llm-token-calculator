"""Anthropic tokenizer implementation."""

from typing import List, Optional
from .base import BaseTokenizer


class AnthropicTokenizer(BaseTokenizer):
    """Tokenizer for Anthropic Claude models."""

    def __init__(self, model: str):
        """Initialize the Anthropic tokenizer.

        Args:
            model: The Anthropic model name
        """
        super().__init__(model)
        self.use_approximation = False
        self.client: Optional[object] = None

        # Try to initialize with API key
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if api_key:
            # Use official API for accurate counting
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key)
                self.use_approximation = False
            except ImportError:
                raise ImportError(
                    "anthropic is required for Anthropic tokenization. "
                    "Install it with: pip install anthropic"
                )
        else:
            # Fall back to approximation
            self.use_approximation = True

    def _approximate_token_count(self, text: str) -> int:
        """Approximate token count using character-based heuristic.

        This is a rough approximation based on the observation that
        Claude models typically use ~3.5-4 characters per token for English text.

        Args:
            text: The text to tokenize

        Returns:
            Approximate token count
        """
        if not text:
            return 0

        # Character-based approximation
        # Average: ~3.7 characters per token for Claude models
        char_count = len(text)

        # Adjust for whitespace (tokens include spaces)
        # Words are typically 1 token, punctuation often 1 token
        words = text.split()
        word_count = len(words)

        # Use a weighted average approach:
        # - Base on character count divided by 3.7
        # - Adjust based on word count (typically 1.2-1.5 tokens per word)
        char_based = char_count / 3.7
        word_based = word_count * 1.3

        # Take average of both methods, rounded up
        estimated = int((char_based + word_based) / 2 + 0.5)

        return max(1, estimated)  # Return at least 1 token for non-empty text

    def encode(self, text: str) -> List[int]:
        """Encode text into tokens.

        Args:
            text: The text to encode

        Returns:
            A list of token IDs (approximated as character positions)

        Note:
            Anthropic doesn't provide direct token IDs, so this is an approximation.
        """
        # Anthropic doesn't expose token IDs directly
        # Return approximate representation
        count = self.count_tokens(text)
        return list(range(count))

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the text.

        Args:
            text: The text to tokenize

        Returns:
            The number of tokens
        """
        if self.use_approximation:
            # Use approximation method
            return self._approximate_token_count(text)
        else:
            # Use Anthropic's beta token counting API
            response = self.client.beta.messages.count_tokens(
                model=self.model,
                messages=[{"role": "user", "content": text}]
            )
            return response.input_tokens

    def is_using_approximation(self) -> bool:
        """Check if using approximation instead of API.

        Returns:
            True if using approximation, False if using API
        """
        return self.use_approximation

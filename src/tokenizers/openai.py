"""OpenAI tokenizer implementation."""

from typing import List
from .base import BaseTokenizer


class OpenAITokenizer(BaseTokenizer):
    """Tokenizer for OpenAI models using tiktoken."""

    def __init__(self, model: str):
        """Initialize the OpenAI tokenizer.

        Args:
            model: The OpenAI model name
        """
        super().__init__(model)
        # Lazy import to avoid dependency issues
        try:
            import tiktoken
        except ImportError:
            raise ImportError(
                "tiktoken is required for OpenAI tokenization. "
                "Install it with: pip install tiktoken"
            )

        # Get encoding for the model
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for newer models
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def encode(self, text: str) -> List[int]:
        """Encode text into tokens.

        Args:
            text: The text to encode

        Returns:
            A list of token IDs
        """
        return self.encoding.encode(text)

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the text.

        Args:
            text: The text to tokenize

        Returns:
            The number of tokens
        """
        return len(self.encode(text))

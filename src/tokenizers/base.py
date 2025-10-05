"""Base tokenizer interface."""

from abc import ABC, abstractmethod
from typing import List


class BaseTokenizer(ABC):
    """Abstract base class for all tokenizer implementations."""

    def __init__(self, model: str):
        """Initialize the tokenizer.

        Args:
            model: The model name
        """
        self.model = model

    @abstractmethod
    def encode(self, text: str) -> List[int]:
        """Encode text into tokens.

        Args:
            text: The text to encode

        Returns:
            A list of token IDs
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the text.

        Args:
            text: The text to tokenize

        Returns:
            The number of tokens
        """
        pass

    def get_model_name(self) -> str:
        """Get the model name.

        Returns:
            The model name
        """
        return self.model

"""Tests for TokenCalculator class - Phase 1: Core Infrastructure."""

import pytest
from unittest.mock import Mock, patch
from src.calculator import TokenCalculator


class TestTokenCalculatorInstantiation:
    """Test TokenCalculator instantiation."""

    def test_can_instantiate_calculator(self):
        """Test that TokenCalculator can be instantiated."""
        calculator = TokenCalculator()
        assert calculator is not None
        assert isinstance(calculator, TokenCalculator)


class TestBasicTokenCounting:
    """Test basic token counting functionality."""

    def test_calculate_returns_integer(self):
        """Test that calculate method returns an integer."""
        calculator = TokenCalculator()
        result = calculator.calculate("Hello, world!", model="gpt-4")
        assert isinstance(result, int)
        assert result > 0

    def test_calculate_empty_string(self):
        """Test that empty string returns 0 tokens."""
        calculator = TokenCalculator()
        result = calculator.calculate("", model="gpt-4")
        assert result == 0

    def test_calculate_whitespace_only(self):
        """Test that whitespace-only string returns 0 tokens."""
        calculator = TokenCalculator()
        result = calculator.calculate("   ", model="gpt-4")
        assert result == 0


class TestModelValidation:
    """Test model selection and validation."""

    def test_unsupported_model_raises_error(self):
        """Test that unsupported model raises ValueError."""
        calculator = TokenCalculator()
        with pytest.raises(ValueError, match="Unsupported model"):
            calculator.calculate("Hello", model="invalid-model")

    def test_supported_model_gpt4(self):
        """Test that gpt-4 is a supported model."""
        calculator = TokenCalculator()
        # Should not raise error
        result = calculator.calculate("Hello", model="gpt-4")
        assert isinstance(result, int)

    @patch('anthropic.Anthropic')
    def test_supported_model_claude3(self, mock_anthropic):
        """Test that claude-3-opus is a supported model."""
        # Mock the Anthropic client response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.input_tokens = 2
        mock_client.beta.messages.count_tokens.return_value = mock_response
        mock_anthropic.return_value = mock_client

        calculator = TokenCalculator()
        # Should not raise error
        result = calculator.calculate("Hello", model="claude-3-opus")
        assert isinstance(result, int)
        assert result == 2

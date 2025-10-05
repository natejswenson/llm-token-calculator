"""Tests for tokenizer implementations - Phase 2: OpenAI Tokenizer, Phase 3: Anthropic Tokenizer."""

import pytest
from unittest.mock import Mock, patch
from src.tokenizers.openai import OpenAITokenizer
from src.tokenizers.anthropic import AnthropicTokenizer


class TestOpenAITokenizerInitialization:
    """Test OpenAI tokenizer initialization."""

    def test_can_instantiate_with_gpt4(self):
        """Test that OpenAITokenizer can be instantiated with gpt-4."""
        tokenizer = OpenAITokenizer("gpt-4")
        assert tokenizer is not None
        assert tokenizer.get_model_name() == "gpt-4"

    def test_can_instantiate_with_gpt35_turbo(self):
        """Test that OpenAITokenizer can be instantiated with gpt-3.5-turbo."""
        tokenizer = OpenAITokenizer("gpt-3.5-turbo")
        assert tokenizer is not None
        assert tokenizer.get_model_name() == "gpt-3.5-turbo"


class TestOpenAIKnownTokenCounts:
    """Test known token counts for OpenAI models."""

    def test_gpt4_hello_world(self):
        """Test token count for 'Hello, world!' with gpt-4."""
        tokenizer = OpenAITokenizer("gpt-4")
        # "Hello, world!" should be 4 tokens for GPT-4
        count = tokenizer.count_tokens("Hello, world!")
        assert count == 4

    def test_gpt4_empty_string(self):
        """Test token count for empty string."""
        tokenizer = OpenAITokenizer("gpt-4")
        count = tokenizer.count_tokens("")
        assert count == 0

    def test_gpt4_single_word(self):
        """Test token count for single word 'Hello'."""
        tokenizer = OpenAITokenizer("gpt-4")
        # "Hello" should be 1 token
        count = tokenizer.count_tokens("Hello")
        assert count == 1

    def test_gpt4_longer_text(self):
        """Test token count for longer text."""
        tokenizer = OpenAITokenizer("gpt-4")
        text = "The quick brown fox jumps over the lazy dog"
        count = tokenizer.count_tokens(text)
        # This should be 9 tokens
        assert count == 9


class TestOpenAIEncodingDecoding:
    """Test encoding consistency."""

    def test_encode_returns_list(self):
        """Test that encode returns a list of integers."""
        tokenizer = OpenAITokenizer("gpt-4")
        tokens = tokenizer.encode("Hello, world!")
        assert isinstance(tokens, list)
        assert all(isinstance(t, int) for t in tokens)

    def test_encode_count_consistency(self):
        """Test that encode length matches count_tokens."""
        tokenizer = OpenAITokenizer("gpt-4")
        text = "The quick brown fox"
        tokens = tokenizer.encode(text)
        count = tokenizer.count_tokens(text)
        assert len(tokens) == count


class TestOpenAIModelDifferences:
    """Test that different models may have different tokenization."""

    def test_gpt4_vs_gpt35_turbo(self):
        """Test that gpt-4 and gpt-3.5-turbo may tokenize differently."""
        text = "artificial intelligence"

        tokenizer_gpt4 = OpenAITokenizer("gpt-4")
        tokenizer_gpt35 = OpenAITokenizer("gpt-3.5-turbo")

        count_gpt4 = tokenizer_gpt4.count_tokens(text)
        count_gpt35 = tokenizer_gpt35.count_tokens(text)

        # Both should return integers
        assert isinstance(count_gpt4, int)
        assert isinstance(count_gpt35, int)
        # For this specific case, they should be the same (both use cl100k_base)
        assert count_gpt4 == count_gpt35


# Phase 3: Anthropic Tokenizer Tests
class TestAnthropicTokenizerInitialization:
    """Test Anthropic tokenizer initialization."""

    @patch('anthropic.Anthropic')
    def test_can_instantiate_with_claude3_opus(self, mock_anthropic):
        """Test that AnthropicTokenizer can be instantiated with claude-3-opus."""
        tokenizer = AnthropicTokenizer("claude-3-opus")
        assert tokenizer is not None
        assert tokenizer.get_model_name() == "claude-3-opus"

    @patch('anthropic.Anthropic')
    def test_can_instantiate_with_claude2(self, mock_anthropic):
        """Test that AnthropicTokenizer can be instantiated with claude-2."""
        tokenizer = AnthropicTokenizer("claude-2")
        assert tokenizer is not None
        assert tokenizer.get_model_name() == "claude-2"


class TestAnthropicKnownTokenCounts:
    """Test known token counts for Anthropic models."""

    @patch('anthropic.Anthropic')
    def test_claude3_hello_world(self, mock_anthropic):
        """Test token count for 'Hello, world!' with claude-3-opus."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.input_tokens = 5
        mock_client.beta.messages.count_tokens.return_value = mock_response
        mock_anthropic.return_value = mock_client

        tokenizer = AnthropicTokenizer("claude-3-opus")
        count = tokenizer.count_tokens("Hello, world!")
        assert count == 5

    @patch('anthropic.Anthropic')
    def test_claude3_empty_string(self, mock_anthropic):
        """Test token count for empty string."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.input_tokens = 0
        mock_client.beta.messages.count_tokens.return_value = mock_response
        mock_anthropic.return_value = mock_client

        tokenizer = AnthropicTokenizer("claude-3-opus")
        count = tokenizer.count_tokens("")
        assert count == 0


class TestAnthropicModelSpecific:
    """Test Anthropic model-specific behavior."""

    @patch('anthropic.Anthropic')
    def test_count_tokens_calls_api_correctly(self, mock_anthropic):
        """Test that count_tokens calls the Anthropic API with correct parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.input_tokens = 10
        mock_client.beta.messages.count_tokens.return_value = mock_response
        mock_anthropic.return_value = mock_client

        tokenizer = AnthropicTokenizer("claude-3-sonnet")
        text = "Test message"
        count = tokenizer.count_tokens(text)

        # Verify the API was called with correct parameters
        mock_client.beta.messages.count_tokens.assert_called_once_with(
            model="claude-3-sonnet",
            messages=[{"role": "user", "content": text}]
        )
        assert count == 10

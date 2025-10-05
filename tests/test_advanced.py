"""Tests for advanced features - Phase 5."""

import pytest
from src.calculator import TokenCalculator


class TestBatchProcessing:
    """Test batch processing of multiple texts."""

    def test_calculate_detailed_returns_dict(self):
        """Test that calculate_detailed returns a dictionary."""
        calculator = TokenCalculator()
        result = calculator.calculate_detailed("Hello, world!", model="gpt-4")
        assert isinstance(result, dict)
        assert "token_count" in result
        assert "model" in result
        assert "character_count" in result

    def test_calculate_detailed_correct_values(self):
        """Test that calculate_detailed returns correct values."""
        calculator = TokenCalculator()
        text = "Hello, world!"
        result = calculator.calculate_detailed(text, model="gpt-4")

        assert result["token_count"] == 4
        assert result["model"] == "gpt-4"
        assert result["character_count"] == len(text)

    def test_batch_calculate_multiple_texts(self):
        """Test calculating tokens for multiple texts."""
        calculator = TokenCalculator()
        texts = [
            "Hello",
            "World",
            "The quick brown fox"
        ]

        results = [calculator.calculate(text, "gpt-4") for text in texts]

        assert len(results) == 3
        assert all(isinstance(r, int) for r in results)
        assert results[0] == 1  # "Hello"
        assert results[1] == 1  # "World"
        assert results[2] == 4  # "The quick brown fox"


class TestTokenizerCaching:
    """Test tokenizer caching for performance."""

    def test_tokenizer_reuse(self):
        """Test that tokenizers are cached and reused."""
        calculator = TokenCalculator()

        # First call creates tokenizer
        count1 = calculator.calculate("Hello", "gpt-4")

        # Second call should reuse cached tokenizer
        count2 = calculator.calculate("World", "gpt-4")

        # Verify tokenizer was cached
        assert "gpt-4" in calculator._tokenizers
        assert isinstance(count1, int)
        assert isinstance(count2, int)

    def test_multiple_model_caching(self):
        """Test that different models are cached separately."""
        calculator = TokenCalculator()

        calculator.calculate("Hello", "gpt-4")
        calculator.calculate("Hello", "gpt-3.5-turbo")

        # Both tokenizers should be cached
        assert "gpt-4" in calculator._tokenizers
        assert "gpt-3.5-turbo" in calculator._tokenizers


class TestLargeInputs:
    """Test handling of large text inputs."""

    def test_large_text_processing(self):
        """Test processing large text input."""
        calculator = TokenCalculator()
        # Create a large text (50k characters)
        large_text = "Hello world. " * 4000

        result = calculator.calculate(large_text, "gpt-4")
        assert isinstance(result, int)
        assert result > 0

    def test_very_long_single_line(self):
        """Test processing very long single line."""
        calculator = TokenCalculator()
        # Create a very long line
        long_line = "x" * 10000

        result = calculator.calculate(long_line, "gpt-4")
        assert isinstance(result, int)
        assert result > 0


class TestMarkdownIntegration:
    """Test markdown preprocessing integration."""

    def test_markdown_preprocessing_enabled_by_default(self):
        """Test that markdown preprocessing is enabled by default."""
        calculator = TokenCalculator()
        markdown_text = "# Hello\n\n**World**"

        result = calculator.calculate(markdown_text, "gpt-4")
        # Should process markdown and count tokens
        assert isinstance(result, int)

    def test_markdown_preprocessing_can_be_disabled(self):
        """Test that markdown preprocessing can be disabled."""
        calculator = TokenCalculator(preprocess_markdown=False)
        markdown_text = "# Hello\n\n**World**"

        result = calculator.calculate(markdown_text, "gpt-4")
        # Should count raw markdown tokens
        assert isinstance(result, int)

    def test_markdown_vs_plain_different_counts(self):
        """Test that markdown and plain text may have different counts."""
        calc_with_md = TokenCalculator(preprocess_markdown=True)
        calc_without_md = TokenCalculator(preprocess_markdown=False)

        markdown_text = "# **Bold Title**"

        count_with = calc_with_md.calculate(markdown_text, "gpt-4")
        count_without = calc_without_md.calculate(markdown_text, "gpt-4")

        # Both should be integers
        assert isinstance(count_with, int)
        assert isinstance(count_without, int)
        # The counts may differ
        assert count_with != count_without


class TestFileContentProcessing:
    """Test processing file content."""

    def test_calculate_from_file_content(self):
        """Test calculating tokens from file content."""
        calculator = TokenCalculator()

        # Simulate reading from markdown file
        with open("tests/fixtures/sample_markdown.md", "r") as f:
            content = f.read()

        result = calculator.calculate(content, "gpt-4")
        assert isinstance(result, int)
        assert result > 0

    def test_detailed_from_file_content(self):
        """Test detailed calculation from file content."""
        calculator = TokenCalculator()

        with open("tests/fixtures/sample_markdown.md", "r") as f:
            content = f.read()

        result = calculator.calculate_detailed(content, "gpt-4")
        assert result["token_count"] > 0
        assert result["character_count"] == len(content)
        assert result["model"] == "gpt-4"

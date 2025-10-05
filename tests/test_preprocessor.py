"""Tests for markdown preprocessing - Phase 4: Markdown Processing."""

import pytest
from src.preprocessor import MarkdownPreprocessor


class TestMarkdownPreprocessorBasic:
    """Test basic markdown preprocessing."""

    def test_can_instantiate_preprocessor(self):
        """Test that MarkdownPreprocessor can be instantiated."""
        preprocessor = MarkdownPreprocessor()
        assert preprocessor is not None

    def test_process_plain_text(self):
        """Test processing plain text without markdown."""
        preprocessor = MarkdownPreprocessor()
        text = "This is plain text"
        result = preprocessor.process(text)
        assert result == "This is plain text"


class TestMarkdownHeaders:
    """Test markdown header conversion."""

    def test_process_h1_header(self):
        """Test processing H1 header."""
        preprocessor = MarkdownPreprocessor()
        text = "# Title"
        result = preprocessor.process(text)
        assert "Title" in result

    def test_process_h2_header(self):
        """Test processing H2 header."""
        preprocessor = MarkdownPreprocessor()
        text = "## Subtitle"
        result = preprocessor.process(text)
        assert "Subtitle" in result

    def test_process_multiple_headers(self):
        """Test processing multiple headers."""
        preprocessor = MarkdownPreprocessor()
        text = "# Main Title\n\n## Section 1\n\n### Subsection"
        result = preprocessor.process(text)
        assert "Main Title" in result
        assert "Section 1" in result
        assert "Subsection" in result


class TestMarkdownFormatting:
    """Test markdown formatting conversion."""

    def test_process_bold_text(self):
        """Test processing bold text."""
        preprocessor = MarkdownPreprocessor()
        text = "This is **bold** text"
        result = preprocessor.process(text)
        assert "bold" in result

    def test_process_italic_text(self):
        """Test processing italic text."""
        preprocessor = MarkdownPreprocessor()
        text = "This is *italic* text"
        result = preprocessor.process(text)
        assert "italic" in result

    def test_process_combined_formatting(self):
        """Test processing combined bold and italic."""
        preprocessor = MarkdownPreprocessor()
        text = "**bold** and *italic* text"
        result = preprocessor.process(text)
        assert "bold" in result
        assert "italic" in result


class TestMarkdownCodeBlocks:
    """Test code block handling."""

    def test_process_inline_code(self):
        """Test processing inline code."""
        preprocessor = MarkdownPreprocessor()
        text = "Use `print()` function"
        result = preprocessor.process(text)
        assert "print()" in result

    def test_process_code_block(self):
        """Test processing code blocks."""
        preprocessor = MarkdownPreprocessor()
        text = "```python\nprint('hello')\n```"
        result = preprocessor.process(text)
        assert "print('hello')" in result

    def test_process_code_block_preserves_content(self):
        """Test that code block content is preserved."""
        preprocessor = MarkdownPreprocessor()
        text = "```\ndef foo():\n    return True\n```"
        result = preprocessor.process(text)
        assert "foo()" in result


class TestMarkdownLinks:
    """Test link and image syntax processing."""

    def test_process_link(self):
        """Test processing markdown links."""
        preprocessor = MarkdownPreprocessor()
        text = "[Google](https://google.com)"
        result = preprocessor.process(text)
        # Should extract the link text
        assert "Google" in result

    def test_process_image(self):
        """Test processing markdown images."""
        preprocessor = MarkdownPreprocessor()
        text = "![Alt text](image.png)"
        result = preprocessor.process(text)
        # Should extract alt text
        assert "Alt text" in result


class TestMarkdownComplexContent:
    """Test complex markdown content."""

    def test_process_mixed_content(self):
        """Test processing markdown with mixed formatting."""
        preprocessor = MarkdownPreprocessor()
        text = """# Title

This is a paragraph with **bold** and *italic* text.

## Code Example

```python
print('hello')
```

- List item 1
- List item 2
"""
        result = preprocessor.process(text)
        assert "Title" in result
        assert "bold" in result
        assert "italic" in result
        assert "print('hello')" in result
        assert "List item 1" in result

    def test_process_preserves_meaningful_whitespace(self):
        """Test that meaningful whitespace is preserved."""
        preprocessor = MarkdownPreprocessor()
        text = "Line 1\n\nLine 2"
        result = preprocessor.process(text)
        # Should preserve paragraph separation
        assert "Line 1" in result
        assert "Line 2" in result


class TestMarkdownEdgeCases:
    """Test edge cases."""

    def test_process_empty_string(self):
        """Test processing empty string."""
        preprocessor = MarkdownPreprocessor()
        result = preprocessor.process("")
        assert result == ""

    def test_process_only_whitespace(self):
        """Test processing whitespace only."""
        preprocessor = MarkdownPreprocessor()
        result = preprocessor.process("   \n\n   ")
        # Should return minimal whitespace
        assert len(result.strip()) == 0

    def test_process_special_characters(self):
        """Test processing special characters."""
        preprocessor = MarkdownPreprocessor()
        text = "Special chars: @#$%^&*()"
        result = preprocessor.process(text)
        assert "@#$%^&*()" in result

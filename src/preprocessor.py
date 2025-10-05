"""Markdown preprocessing module."""

import re


class MarkdownPreprocessor:
    """Processes markdown text for tokenization."""

    def process(self, text: str) -> str:
        """Process markdown text and convert to plain text.

        Args:
            text: The markdown text to process

        Returns:
            Processed plain text
        """
        if not text:
            return ""

        # Create a working copy
        result = text

        # Remove markdown headers (keep the text, remove the #)
        result = re.sub(r'^#{1,6}\s+', '', result, flags=re.MULTILINE)

        # Remove bold markers (keep the text)
        result = re.sub(r'\*\*(.+?)\*\*', r'\1', result)

        # Remove italic markers (keep the text)
        result = re.sub(r'\*(.+?)\*', r'\1', result)

        # Remove inline code markers (keep the text)
        result = re.sub(r'`(.+?)`', r'\1', result)

        # Remove code block markers (keep the code)
        result = re.sub(r'^```[\w]*\n', '', result, flags=re.MULTILINE)
        result = re.sub(r'^```$', '', result, flags=re.MULTILINE)

        # Remove link syntax, keep link text
        result = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', result)

        # Remove image syntax, keep alt text
        result = re.sub(r'!\[([^\]]+)\]\([^\)]+\)', r'\1', result)

        return result

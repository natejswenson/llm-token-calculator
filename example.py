#!/usr/bin/env python3
"""Token Calculator CLI - Calculate tokens for text or file input."""

import argparse
import sys
from pathlib import Path
from src.calculator import TokenCalculator


def main():
    """Run token calculator with command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Calculate token count for text or file using specified LLM model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate tokens for text
  %(prog)s --model gpt-4 --input "Hello, world!"

  # Calculate tokens from file
  %(prog)s --model claude-3-opus --input path/to/file.md

  # Disable markdown preprocessing
  %(prog)s --model gpt-4 --input "# Title" --no-preprocess

  # Get detailed output
  %(prog)s --model gpt-4 --input "Hello" --detailed

Supported models:
  OpenAI:    gpt-4, gpt-4-turbo, gpt-3.5-turbo, text-embedding-ada-002
  Anthropic: claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-2
        """
    )

    parser.add_argument(
        "--model", "-m",
        required=True,
        help="LLM model to use for tokenization (e.g., gpt-4, claude-3-opus)"
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Text to tokenize, or path to file containing text"
    )

    parser.add_argument(
        "--no-preprocess",
        action="store_true",
        help="Disable markdown preprocessing"
    )

    parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="Show detailed output including character count"
    )

    args = parser.parse_args()

    # Determine if input is a file or text
    input_path = Path(args.input)
    if input_path.exists() and input_path.is_file():
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()
            input_source = f"file: {args.input}"
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.input
        input_source = "text"

    # Initialize calculator
    calculator = TokenCalculator(preprocess_markdown=not args.no_preprocess)

    # Calculate tokens
    try:
        if args.detailed:
            result = calculator.calculate_detailed(text, model=args.model)
            print(f"Input: {input_source}")
            print(f"Model: {result['model']}")
            print(f"Tokens: {result['token_count']}")
            print(f"Characters: {result['character_count']}")
        else:
            count = calculator.calculate(text, model=args.model)
            print(count)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

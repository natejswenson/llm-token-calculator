# Token Calculator Service Specification

## 1. Overview
A Python service that calculates the number of tokens in text input for various LLM models. The service accepts markdown file content as a string and returns token counts.

## 2. Requirements

### 2.1 Functional Requirements
- **FR1**: Accept text input (from markdown files or plain strings)
- **FR2**: Calculate token count for specified LLM models
- **FR3**: Support multiple LLM tokenizer types (OpenAI, Anthropic, etc.)
- **FR4**: Return accurate token counts based on model-specific tokenization
- **FR5**: Handle markdown formatting and convert to appropriate text representation
- **FR6**: Provide clear API for programmatic usage

### 2.2 Non-Functional Requirements
- **NFR1**: Fast tokenization (<100ms for typical prompts)
- **NFR2**: Memory efficient for large text inputs
- **NFR3**: Easy to extend with new model support
- **NFR4**: Clear error handling and validation
- **NFR5**: Well-documented API and usage examples

## 3. TDD Plan

### 3.1 Red-Green-Refactor Cycle
1. **Red**: Write failing test for specific functionality
2. **Green**: Implement minimal code to pass the test
3. **Refactor**: Improve code quality while keeping tests green

### 3.2 Test Categories

#### Unit Tests
- Tokenizer initialization for different models
- Text preprocessing and markdown handling
- Token counting accuracy for known inputs
- Error handling for invalid inputs
- Model selection and validation

#### Integration Tests
- End-to-end token calculation workflow
- Multiple model support in single session
- File content processing pipeline

#### Edge Case Tests
- Empty string input
- Very large text inputs (>100k characters)
- Special characters and unicode
- Malformed markdown
- Unsupported model requests

## 4. Architecture Design

### 4.1 Components

```
token-calculator/
├── src/
│   ├── __init__.py
│   ├── calculator.py          # Main TokenCalculator class
│   ├── tokenizers/
│   │   ├── __init__.py
│   │   ├── base.py           # Base tokenizer interface
│   │   ├── openai.py         # OpenAI tokenizer implementation
│   │   └── anthropic.py      # Anthropic tokenizer implementation
│   ├── preprocessor.py       # Markdown/text preprocessing
│   └── models.py             # Model configuration and constants
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_tokenizers.py
│   ├── test_preprocessor.py
│   └── fixtures/
│       └── sample_markdown.md
├── requirements.txt
├── setup.py
└── README.md
```

### 4.2 Key Classes

#### TokenCalculator
- Main entry point for token calculation
- Methods: `calculate(text, model)`, `calculate_from_file(filepath, model)`
- Manages tokenizer instances

#### BaseTokenizer (Abstract)
- Interface for all tokenizer implementations
- Methods: `encode(text)`, `count_tokens(text)`, `get_model_name()`

#### MarkdownPreprocessor
- Converts markdown to plain text or preserves formatting as needed
- Handles special markdown syntax

## 5. Implementation Phases

### Phase 1: Core Infrastructure (TDD)
**Tests to write first:**
1. Test TokenCalculator instantiation
2. Test basic token counting with hardcoded tokenizer
3. Test model selection validation

**Implementation:**
- Create TokenCalculator class skeleton
- Implement basic token counting with simple whitespace splitting (temporary)
- Add model validation

### Phase 2: OpenAI Tokenizer Support (TDD)
**Tests to write first:**
1. Test OpenAI tokenizer initialization (gpt-4, gpt-3.5-turbo)
2. Test known token counts for sample texts
3. Test encoding/decoding consistency

**Implementation:**
- Integrate tiktoken library
- Implement OpenAITokenizer class
- Add model mapping (gpt-4, gpt-3.5-turbo, etc.)

### Phase 3: Anthropic Tokenizer Support (TDD)
**Tests to write first:**
1. Test Anthropic tokenizer initialization (claude-3, claude-2)
2. Test known token counts for sample texts
3. Test model-specific differences

**Implementation:**
- Integrate anthropic tokenization library
- Implement AnthropicTokenizer class
- Add Claude model mappings

### Phase 4: Markdown Processing (TDD)
**Tests to write first:**
1. Test markdown headers conversion
2. Test code block handling
3. Test link and image syntax processing
4. Test preservation of meaningful whitespace

**Implementation:**
- Create MarkdownPreprocessor class
- Implement markdown parsing and text extraction
- Handle edge cases (nested structures, escaping)

### Phase 5: Advanced Features (TDD)
**Tests to write first:**
1. Test batch processing multiple texts
2. Test streaming large files
3. Test caching for repeated calculations

**Implementation:**
- Add batch calculation methods
- Optimize for large inputs
- Implement optional caching layer

## 6. Testing Strategy

### 6.1 Test Data
- Known token counts from official model documentation
- Sample markdown files with varying complexity
- Edge cases: empty, very large, special characters

### 6.2 Test Fixtures
```python
# Example test fixture
SAMPLE_TEXTS = {
    "simple": "Hello, world!",
    "markdown": "# Title\n\nParagraph with **bold** and *italic*.",
    "code": "```python\nprint('hello')\n```",
    "large": "..." * 10000
}

EXPECTED_TOKENS = {
    ("simple", "gpt-4"): 4,
    ("simple", "claude-3"): 5,
    # ... more mappings
}
```

### 6.3 Coverage Goals
- Minimum 90% code coverage
- 100% coverage for core tokenization logic
- All error paths tested

## 7. API Design

### 7.1 Basic Usage
```python
from token_calculator import TokenCalculator

calculator = TokenCalculator()

# Calculate tokens for specific model
count = calculator.calculate("Your text here", model="gpt-4")

# Calculate from markdown file content
markdown_content = "# Title\n\nContent..."
count = calculator.calculate(markdown_content, model="claude-3-opus")

# Get detailed information
result = calculator.calculate_detailed("Your text", model="gpt-4")
# Returns: {"token_count": 4, "model": "gpt-4", "character_count": 14}
```

### 7.2 Supported Models
- OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo, text-embedding-ada-002
- Anthropic: claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-2
- Extensible for future models

## 8. Dependencies

### 8.1 Required Libraries
- `tiktoken` - OpenAI tokenization
- `anthropic` - Anthropic tokenization
- `markdown` - Markdown parsing (optional, for preprocessing)

### 8.2 Development Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `mypy` - Type checking
- `ruff` - Linting

## 9. Definition of Done

### For Each Phase:
- [ ] All tests written before implementation
- [ ] All tests passing (green)
- [ ] Code refactored for clarity and maintainability
- [ ] Code coverage meets minimum threshold (90%)
- [ ] Type hints added to all functions
- [ ] Docstrings added to all public methods
- [ ] No linting errors

### For Complete Project:
- [ ] All 5 phases completed
- [ ] Integration tests passing
- [ ] Documentation complete (README, API docs)
- [ ] Example usage scripts provided
- [ ] Performance benchmarks documented
- [ ] Error handling comprehensive and tested

## 10. Acceptance Criteria

### AC1: Basic Token Counting
**Given** a user provides text "Hello, world!"
**When** they request token count for "gpt-4"
**Then** the service returns the correct token count (4)

### AC2: Markdown Processing
**Given** a user provides markdown content with headers and formatting
**When** they request token count
**Then** the service correctly processes markdown and returns accurate count

### AC3: Multiple Model Support
**Given** a user calculates tokens for the same text
**When** they specify different models (gpt-4 vs claude-3)
**Then** different token counts are returned reflecting model-specific tokenization

### AC4: Error Handling
**Given** a user requests an unsupported model
**When** the service processes the request
**Then** a clear error message is returned

### AC5: Performance
**Given** a user provides a large text input (50k characters)
**When** token calculation is performed
**Then** results are returned in less than 100ms

## 11. Development Workflow

### 11.1 TDD Cycle for Each Feature
1. Write test case(s) for new feature
2. Run tests - confirm they fail (RED)
3. Write minimal implementation
4. Run tests - confirm they pass (GREEN)
5. Refactor code for quality
6. Run tests - confirm still passing
7. Commit changes

### 11.2 Git Workflow
- Feature branches for each phase
- Commit after each RED-GREEN-REFACTOR cycle
- Pull request with test results before merging

## 12. Future Enhancements
- CLI interface for command-line usage
- REST API wrapper for HTTP access
- Support for additional models (Llama, Mistral, etc.)
- Token usage estimation and cost calculation
- Batch file processing
- Configuration file support

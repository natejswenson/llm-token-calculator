# Token Calculator Frontend Specification

## 1. Overview
A clean, modern, and simple web frontend for the Token Calculator service. The interface allows users to input text or upload files and calculate token counts for various LLM models.

## 2. Requirements

### 2.1 Functional Requirements
- **FR1**: Display input area for text entry (textarea)
- **FR2**: Support file upload for markdown/text files
- **FR3**: Dropdown to select LLM model
- **FR4**: Calculate and display token count
- **FR5**: Show detailed information (tokens, characters, model)
- **FR6**: Toggle markdown preprocessing on/off
- **FR7**: Clear/reset functionality
- **FR8**: Copy results to clipboard
- **FR9**: Responsive design for mobile and desktop

### 2.2 Non-Functional Requirements
- **NFR1**: Clean, minimal UI design
- **NFR2**: Fast response time (<500ms for typical inputs)
- **NFR3**: Accessible (WCAG 2.1 AA compliance)
- **NFR4**: Works without JavaScript frameworks (vanilla JS or lightweight)
- **NFR5**: No backend server required (calls Python service via API)
- **NFR6**: Browser compatibility (Chrome, Firefox, Safari, Edge)

## 3. TDD Plan

### 3.1 Testing Approach
Since this is a frontend application, we'll use:
- **Unit Tests**: Test JavaScript functions with Jest
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test user workflows with Playwright/Cypress

### 3.2 Red-Green-Refactor Cycle
1. **Red**: Write failing test for UI component/function
2. **Green**: Implement minimal code to pass the test
3. **Refactor**: Improve code quality and styling

## 4. Architecture Design

### 4.1 Technology Stack
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid/Flexbox
- **Vanilla JavaScript**: No heavy frameworks
- **Backend Integration**: REST API calls to Python Flask/FastAPI service

### 4.2 Project Structure

```
frontend/
├── index.html                 # Main HTML page
├── css/
│   ├── styles.css            # Main stylesheet
│   └── reset.css             # CSS reset
├── js/
│   ├── app.js                # Main application logic
│   ├── api.js                # API communication
│   └── utils.js              # Utility functions
├── tests/
│   ├── app.test.js           # App logic tests
│   └── api.test.js           # API tests
├── assets/
│   └── icons/                # UI icons
└── README.md
```

### 4.3 Component Breakdown

#### Main Components
1. **Header**: Title and description
2. **Input Section**:
   - Textarea for text input
   - File upload button
   - Character counter
3. **Settings Panel**:
   - Model selector dropdown
   - Markdown preprocessing toggle
4. **Action Buttons**:
   - Calculate button
   - Clear button
5. **Results Display**:
   - Token count (large, prominent)
   - Character count
   - Model used
   - Copy to clipboard button
6. **Footer**: Credits and links

## 5. Implementation Phases

### Phase 1: HTML Structure & Styling (TDD)
**Tests to write first:**
1. Test HTML contains required elements (textarea, select, buttons)
2. Test CSS grid/flexbox layout responsiveness
3. Test accessibility attributes (ARIA labels, roles)

**Implementation:**
- Create semantic HTML structure
- Implement CSS with mobile-first approach
- Add CSS variables for theming
- Ensure responsive design breakpoints

### Phase 2: API Integration Module (TDD)
**Tests to write first:**
1. Test API call function with mock responses
2. Test error handling for API failures
3. Test request formatting

**Implementation:**
- Create `api.js` module for backend communication
- Implement `calculateTokens(text, model, preprocess)` function
- Add error handling and retry logic
- Mock API endpoint for testing

### Phase 3: Core Application Logic (TDD)
**Tests to write first:**
1. Test text input handling
2. Test file upload and reading
3. Test model selection
4. Test form validation
5. Test clear/reset functionality

**Implementation:**
- Create event listeners for user interactions
- Implement file reading with FileReader API
- Add input validation
- Update UI state management

### Phase 4: Results Display (TDD)
**Tests to write first:**
1. Test results rendering with mock data
2. Test copy to clipboard functionality
3. Test error message display
4. Test loading state indicators

**Implementation:**
- Create results display component
- Add loading spinner/indicator
- Implement copy to clipboard
- Add success/error notifications

### Phase 5: Polish & Enhancements (TDD)
**Tests to write first:**
1. Test keyboard shortcuts
2. Test dark mode toggle
3. Test animation/transitions
4. Test performance with large inputs

**Implementation:**
- Add keyboard shortcuts (Ctrl+Enter to calculate)
- Implement dark mode with CSS custom properties
- Add smooth transitions and micro-interactions
- Optimize performance for large text inputs

## 6. UI/UX Design

### 6.1 Layout
```
┌─────────────────────────────────────────────┐
│           Token Calculator                   │
│   Calculate tokens for any LLM model        │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │                                       │ │
│  │  Text Input Area (Textarea)          │ │
│  │                                       │ │
│  │                                       │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  [📁 Upload File]        1,234 characters   │
│                                             │
│  Model: [gpt-4 ▼]  □ Preprocess Markdown   │
│                                             │
│  [Calculate]  [Clear]                       │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │         Results                       │ │
│  │                                       │ │
│  │         🎯 234 tokens                 │ │
│  │                                       │ │
│  │    Model: gpt-4                       │ │
│  │    Characters: 1,234                  │ │
│  │                                       │ │
│  │    [📋 Copy]                          │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

### 6.2 Color Scheme (Light Mode)
- **Primary**: `#4F46E5` (Indigo)
- **Secondary**: `#10B981` (Green)
- **Background**: `#FFFFFF` (White)
- **Surface**: `#F9FAFB` (Light Gray)
- **Text Primary**: `#111827` (Dark Gray)
- **Text Secondary**: `#6B7280` (Medium Gray)
- **Border**: `#E5E7EB` (Light Border)

### 6.3 Color Scheme (Dark Mode)
- **Primary**: `#6366F1` (Light Indigo)
- **Secondary**: `#34D399` (Light Green)
- **Background**: `#111827` (Dark Gray)
- **Surface**: `#1F2937` (Medium Dark)
- **Text Primary**: `#F9FAFB` (Light)
- **Text Secondary**: `#D1D5DB` (Light Gray)
- **Border**: `#374151` (Dark Border)

### 6.4 Typography
- **Font Family**: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- **Heading**: 24px, 600 weight
- **Body**: 16px, 400 weight
- **Small**: 14px, 400 weight
- **Token Display**: 48px, 700 weight (results)

## 7. API Integration

### 7.1 Backend API Endpoints
The frontend will communicate with a Python backend (Flask/FastAPI):

```
POST /api/calculate
Request:
{
  "text": "string",
  "model": "gpt-4",
  "preprocess_markdown": true
}

Response:
{
  "token_count": 234,
  "character_count": 1234,
  "model": "gpt-4"
}
```

### 7.2 Error Handling
- Network errors: Show "Unable to connect" message
- Invalid model: Show "Unsupported model" message
- Large input: Show "Text too large" warning
- API errors: Show specific error message from backend

## 8. Testing Strategy

### 8.1 Unit Tests (Jest)
```javascript
// Example test structure
describe('TokenCalculator', () => {
  describe('calculateTokens', () => {
    it('should call API with correct parameters', async () => {
      // Test API call
    });

    it('should handle API errors gracefully', async () => {
      // Test error handling
    });
  });

  describe('File Upload', () => {
    it('should read file content correctly', async () => {
      // Test file reading
    });
  });
});
```

### 8.2 E2E Tests (Playwright)
```javascript
test('user can calculate tokens for text input', async ({ page }) => {
  await page.goto('/');
  await page.fill('textarea', 'Hello, world!');
  await page.selectOption('select[name="model"]', 'gpt-4');
  await page.click('button:text("Calculate")');
  await expect(page.locator('.result')).toContainText('4 tokens');
});
```

### 8.3 Coverage Goals
- Minimum 80% code coverage
- 100% coverage for API communication
- All user workflows tested with E2E tests

## 9. Definition of Done

### For Each Phase:
- [ ] All tests written before implementation
- [ ] All tests passing
- [ ] Code is accessible (keyboard navigation, ARIA labels)
- [ ] Responsive on mobile and desktop
- [ ] Cross-browser tested
- [ ] No console errors or warnings
- [ ] Lighthouse score >90 (Performance, Accessibility)

### For Complete Project:
- [ ] All 5 phases completed
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Documentation complete
- [ ] Dark mode implemented
- [ ] Deployed and accessible

## 10. Acceptance Criteria

### AC1: Text Input and Calculation
**Given** a user enters "Hello, world!" in the textarea
**When** they select "gpt-4" and click Calculate
**Then** the result shows "4 tokens"

### AC2: File Upload
**Given** a user uploads a markdown file
**When** the file is processed
**Then** the textarea is populated with file content

### AC3: Model Selection
**Given** a user selects different models
**When** calculating the same text
**Then** different token counts are displayed (if applicable)

### AC4: Markdown Preprocessing Toggle
**Given** a user enters markdown text
**When** they toggle preprocessing on/off
**Then** token counts differ based on preprocessing

### AC5: Responsive Design
**Given** a user accesses the app on mobile
**When** they interact with the interface
**Then** all elements are usable and properly sized

### AC6: Copy to Clipboard
**Given** calculation results are displayed
**When** user clicks "Copy"
**Then** results are copied to clipboard and confirmation shown

### AC7: Error Handling
**Given** API is unavailable
**When** user tries to calculate
**Then** clear error message is displayed

### AC8: Accessibility
**Given** a keyboard-only user
**When** they navigate the interface
**Then** all functionality is accessible via keyboard

## 11. Implementation Details

### 11.1 File Upload Implementation
```javascript
// Read file content
function handleFileUpload(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const content = e.target.result;
    document.getElementById('textInput').value = content;
    updateCharacterCount();
  };
  reader.readAsText(file);
}
```

### 11.2 API Call Implementation
```javascript
// Calculate tokens via API
async function calculateTokens(text, model, preprocess) {
  try {
    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, model, preprocess_markdown: preprocess })
    });

    if (!response.ok) throw new Error('API request failed');

    return await response.json();
  } catch (error) {
    throw new Error('Unable to calculate tokens: ' + error.message);
  }
}
```

### 11.3 Results Display
```javascript
// Update UI with results
function displayResults(data) {
  document.getElementById('tokenCount').textContent = data.token_count;
  document.getElementById('charCount').textContent = data.character_count;
  document.getElementById('modelUsed').textContent = data.model;
  document.getElementById('results').classList.remove('hidden');
}
```

## 12. Backend Service Requirements

### 12.1 Python Flask/FastAPI Server
A simple REST API wrapper around the existing token calculator:

```python
# Example Flask endpoint
@app.route('/api/calculate', methods=['POST'])
def calculate_tokens():
    data = request.json
    calculator = TokenCalculator(
        preprocess_markdown=data.get('preprocess_markdown', True)
    )

    result = calculator.calculate_detailed(
        text=data['text'],
        model=data['model']
    )

    return jsonify(result)
```

### 12.2 CORS Configuration
Enable CORS for frontend-backend communication during development.

## 13. Performance Optimization

### 13.1 Debouncing
- Debounce character counter updates (300ms)
- Debounce auto-calculation if implemented (1000ms)

### 13.2 Lazy Loading
- Load results section only after first calculation
- Defer non-critical scripts

### 13.3 Caching
- Cache model list from backend
- Store user preferences in localStorage

## 14. Future Enhancements
- Batch processing (multiple texts)
- History of calculations
- Export results to CSV/JSON
- Comparison mode (multiple models side-by-side)
- Syntax highlighting for code blocks
- PWA support for offline usage
- API key management for Anthropic models

## 15. Deployment

### 15.1 Static Hosting
- Deploy frontend to Netlify, Vercel, or GitHub Pages
- Backend API to Heroku, Railway, or cloud provider

### 15.2 Environment Variables
```
BACKEND_API_URL=https://api.example.com
ANTHROPIC_API_KEY=sk-xxx (backend only)
```

## 16. Success Metrics
- Time to first calculation < 2 seconds
- User can complete calculation workflow in < 30 seconds
- Mobile usage accounts for >40% of traffic
- Zero critical accessibility issues
- Page load time < 1.5 seconds

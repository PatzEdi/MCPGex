# MCPGex

This is an MCP (Model Context Protocol) server that allows LLMs to test and validate regex patterns against test cases. It provides a systematic way to develop regex patterns by defining expected outcomes and iteratively testing patterns until all requirements are satisfied.

## How it works

1. **Define test cases**: You provide examples consisting of input strings and the expected matches/extractions that the regex should produce.
2. **Test patterns**: The LLM can test different regex patterns against all defined test cases to see which ones pass or fail.
3. **Iterate**: Based on the results, the LLM can refine the regex pattern until all test cases pass.
4. **Validate**: Once all tests pass, you have a regex pattern that works for your specific use cases.

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

Start the MCP server:
```bash
python server.py
```

The server will run using stdin/stdout and can be connected to by any MCP-compatible client.

### Configuration
You can also add a configuration. For example, for Claude Desktop, you can have:
```json
{
  "mcpServers": {
    "regex-mcp": {
      "command": "python3",
      "args": ["/absolute/path/to/MCP/RegexMCP/server.py"],
      "cwd": "absolute/path/to/MCP/RegexMCP"
    }
  }
}
```
Or, for other applications, such as Zed:

```json
"context_servers": {
  "regex-mcp-server": {
    "command": {
      "path": "/path/to/python3",
      "args": ["/absolute/path/to/MCP/RegexMCP/server.py"],
      "env": {}
    },
    "settings": {}
  }
}
```
Then, you will be able to use the server in these tools without having to run the python script manually!

### Available Tools

The server provides four main tools:

#### 1. `add_test_case`
Add a new test case with an input string and expected match.

**Parameters:**
- `input_string` (required): The text to test against
- `expected_match` (required): The substring that should be extracted/matched
- `description` (optional): Description of what this test case validates

**Example:**
```json
{
  "input_string": "Contact me at john@example.com for details", 
  "expected_match": "john@example.com",
  "description": "Basic email extraction"
}
```

#### 2. `test_regex`
Test a regex pattern against all current test cases.

**Parameters:**
- `pattern` (required): The regex pattern to test
- `flags` (optional): Regex flags like 'i' (case-insensitive), 'm' (multiline), 's' (dotall)

**Example:**
```json
{
  "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
  "flags": "i"
}
```

#### 3. `get_test_cases`
View all currently defined test cases.

#### 4. `clear_test_cases`
Remove all test cases to start fresh.

## Example Workflow

Here's a typical workflow for developing an email extraction regex:

### Step 1: Define test cases
```json
// Add various email formats you want to support
add_test_case({
  "input_string": "Contact: john.doe@example.com",
  "expected_match": "john.doe@example.com"
})

add_test_case({
  "input_string": "Email me at jane_smith123@company.org", 
  "expected_match": "jane_smith123@company.org"
})

add_test_case({
  "input_string": "Support: help@test-site.co.uk",
  "expected_match": "help@test-site.co.uk"
})
```

### Step 2: Test patterns
```json
// Try a simple pattern first
test_regex({"pattern": "\\w+@\\w+\\.\\w+"})
// Result: Some test cases fail for complex emails

// Try a more comprehensive pattern
test_regex({"pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"})
// Result: All test cases pass! ✅
```

### Step 3: Verify and use
Once all test cases pass, you have a validated regex pattern that works for your specific requirements.

## Common Use Cases

- **Email extraction**: Extract email addresses from text
- **Phone number parsing**: Extract phone numbers in various formats  
- **URL extraction**: Find URLs in content
- **Date parsing**: Extract dates in different formats
- **Data validation**: Validate input formats
- **Log parsing**: Extract specific fields from log entries
- **Text processing**: Extract structured data from unstructured text

## Development

### Running Tests
```bash
pip install pytest pytest-asyncio
pytest tests/
```

### Project Structure
```
RegexMCP/
├── server.py              # Main MCP server implementation
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── example_usage.py      # Usage examples and workflow
├── tests/
│   └── test_server.py    # Test suite
└── README.md            # This file
```

## Benefits

- **Systematic development**: Define requirements before writing regex
- **Comprehensive testing**: Ensure patterns work across all use cases
- **Iterative improvement**: Easy to test and refine patterns
- **Documentation**: Test cases serve as examples and documentation
- **Confidence**: Know your regex works before deploying it

## Requirements

- Python 3.8+
- MCP library (`pip install mcp`)

## License

This project is open source. Feel free to use and modify as needed.



# MCPGex

*MCP server for finding, testing and refining regex patterns*

<div align="center">
<img src="https://github.com/PatzEdi/MCPGex/raw/main/assets/logo.png" alt="mcpgex-high-resolution-logo-transparent" width="500">
</div>

<p align="center">
	<img src="https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square"
		height="23">
	<img src="https://img.shields.io/badge/Creator-PatzEdi-brightgreen?style=flat-square"
		height="23">
</p>

<p align = "center">
	<img src="https://img.shields.io/pypi/v/MCPGex?style=flat-square&color=%23FFA500"
		height="23">
</p>

MCPGex is an MCP server that allows LLMs to test and validate regex patterns against test cases. It provides a systematic way to develop regex patterns by defining or generating expected outcomes and iteratively testing patterns until all requirements are satisfied.

> [!WARNING]
> MCPGex is still in its early stages.

## Index
- [How it works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Configuration](#configuration)
  - [Available Tools](#available-tools-click-to-expand)
- [Benefits](#benefits)
- [Requirements](#requirements-installed-automatically-through-pip3)
- [License](#license)

## How it works

1. **Define the goal**: You provide what the goal regex pattern should return. The LLM will generate test cases for you.
2. **Test patterns**: The LLM can test different regex patterns against all defined test cases to see which ones pass or fail.
3. **Iterate**: Based on the results, the LLM can refine the regex pattern until all test cases pass.
4. **Validate**: Once all tests pass, you have a regex pattern that works for your specific use cases.

## Installation

Go ahead and install through pip:

```bash
pip3 install mcpgex
```

## Usage

### Running the Server

If you want to start the MCP server:
```bash
mcpgex
```

### Configuration
You can also add a configuration. For example, for Claude Desktop, you can have:
```json
{
  "mcpServers": {
    "mcpgex": {
      "command": "python3",
      "args": ["-m", "mcpgex"]
    }
  }
}
```

Or, for other applications, such as Zed:

```json
"context_servers": {
  "mcpgex": {
    "command": {
      "path": "python3",
      "args": ["-m", "mcpgex"]
    },
    "settings": {}
  }
}
```
Then, you will be able to use the server in these tools without having to run the python script manually!

<details>
<summary>

### Available Tools (click to expand)

</summary>

The server provides **four** main tools:

#### 1. `add_test_case`
Add a new test case with an input string and expected match.

**Parameters:**
- `input_string` (required): The text to test against
- `expected_matches` (required): The array of substrings that should be extracted/matched
- `description` (optional): Description of what this test case validates

**Example:**
```json
{
  "input_string": "Contact me at john@example.com for details", 
  "expected_matches": ["john@example.com"],
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

</details>

## Benefits

- **Comprehensive testing**: Ensure patterns work across various use cases
- **Iterative improvement**: Easy to test and refine patterns
- **Documentation**: Test cases serve as examples and documentation
- **Confidence**: Know your regex works before deploying it
- **Fully Automated**: Give it instructions, let it do the rest

## Requirements (installed automatically through pip3)

- Python 3.8+
- MCP library (`pip3 install mcp`)

## License

This project is open source under the MIT license. Feel free to use and modify as needed.

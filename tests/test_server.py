#!/usr/bin/env python3

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import server, test_cases, handle_call_tool
import mcp.types as types


@pytest.fixture(autouse=True)
def clear_test_cases():
    """Clear test cases before each test"""
    test_cases.clear()


class TestRegexMCPServer:
    """Test cases for the Regex MCP Server"""

    @pytest.mark.asyncio
    async def test_add_test_case(self):
        """Test adding a test case"""
        arguments = {
            "input_string": "test@example.com",
            "expected_match": "test@example.com",
            "description": "Email test"
        }

        result = await handle_call_tool("add_test_case", arguments)

        # Check that a TextContent was returned
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Added test case" in result[0].text
        assert "test@example.com" in result[0].text

        # Check that the test case was actually added
        assert len(test_cases) == 1
        assert test_cases[0]["input_string"] == "test@example.com"
        assert test_cases[0]["expected_match"] == "test@example.com"
        assert test_cases[0]["description"] == "Email test"

    @pytest.mark.asyncio
    async def test_add_test_case_without_description(self):
        """Test adding a test case without description"""
        arguments = {
            "input_string": "hello world",
            "expected_match": "hello"
        }

        result = await handle_call_tool("add_test_case", arguments)

        assert len(result) == 1
        assert len(test_cases) == 1
        assert test_cases[0]["description"] == ""

    @pytest.mark.asyncio
    async def test_get_test_cases_empty(self):
        """Test getting test cases when none exist"""
        result = await handle_call_tool("get_test_cases", {})

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "No test cases defined yet" in result[0].text

    @pytest.mark.asyncio
    async def test_get_test_cases_with_data(self):
        """Test getting test cases when some exist"""
        # Add a test case first
        test_cases.append({
            "input_string": "test input",
            "expected_match": "test",
            "description": "sample test"
        })

        result = await handle_call_tool("get_test_cases", {})

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Current test cases" in result[0].text
        assert "test input" in result[0].text
        assert "test" in result[0].text
        assert "sample test" in result[0].text

    @pytest.mark.asyncio
    async def test_clear_test_cases(self):
        """Test clearing test cases"""
        # Add some test cases first
        test_cases.extend([
            {"input_string": "test1", "expected_match": "test1", "description": ""},
            {"input_string": "test2", "expected_match": "test2", "description": ""}
        ])

        assert len(test_cases) == 2

        result = await handle_call_tool("clear_test_cases", {})

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Cleared all test cases" in result[0].text
        assert "Removed 2 test case(s)" in result[0].text
        assert len(test_cases) == 0

    @pytest.mark.asyncio
    async def test_test_regex_no_test_cases(self):
        """Test regex testing when no test cases exist"""
        arguments = {"pattern": r"\w+"}

        result = await handle_call_tool("test_regex", arguments)

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "No test cases defined" in result[0].text

    @pytest.mark.asyncio
    async def test_test_regex_invalid_pattern(self):
        """Test regex testing with invalid pattern"""
        # Add a test case first
        test_cases.append({
            "input_string": "test",
            "expected_match": "test",
            "description": ""
        })

        arguments = {"pattern": r"[invalid"}  # Invalid regex

        result = await handle_call_tool("test_regex", arguments)

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert "Invalid regex pattern" in result[0].text

    @pytest.mark.asyncio
    async def test_test_regex_successful_match(self):
        """Test regex testing with successful pattern"""
        # Add test cases
        test_cases.extend([
            {"input_string": "hello world", "expected_match": "hello", "description": "greeting"},
            {"input_string": "hello there", "expected_match": "hello", "description": "another greeting"}
        ])

        arguments = {"pattern": r"hello"}

        result = await handle_call_tool("test_regex", arguments)

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        text = result[0].text
        assert "Testing regex pattern: hello" in text
        assert "✅" in text  # Should have passing test cases
        assert "2 passed, 0 failed" in text
        assert "All test cases passed" in text

    @pytest.mark.asyncio
    async def test_test_regex_partial_failure(self):
        """Test regex testing with some failures"""
        # Add test cases
        test_cases.extend([
            {"input_string": "hello world", "expected_match": "hello", "description": "should pass"},
            {"input_string": "goodbye world", "expected_match": "goodbye", "description": "should fail"}
        ])

        arguments = {"pattern": r"hello"}

        result = await handle_call_tool("test_regex", arguments)

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        text = result[0].text
        assert "✅" in text  # Should have one passing test
        assert "❌" in text  # Should have one failing test
        assert "1 passed, 1 failed" in text
        assert "Some test cases failed" in text

    @pytest.mark.asyncio
    async def test_test_regex_with_flags(self):
        """Test regex testing with flags"""
        # Add test case with uppercase
        test_cases.append({
            "input_string": "HELLO world",
            "expected_match": "HELLO",
            "description": ""
        })

        arguments = {"pattern": r"hello", "flags": "i"}  # Case insensitive

        result = await handle_call_tool("test_regex", arguments)

        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        text = result[0].text
        assert "Flags: i" in text
        assert "✅" in text  # Should pass with case insensitive flag

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        """Test calling an unknown tool"""
        with pytest.raises(ValueError, match="Unknown tool"):
            await handle_call_tool("unknown_tool", {})

    @pytest.mark.asyncio
    async def test_email_extraction_scenario(self):
        """Test a complete email extraction scenario"""
        # Add email test cases
        email_cases = [
            {"input_string": "Contact: john@example.com", "expected_match": "john@example.com", "description": "Basic email"},
            {"input_string": "Email me at test.user@domain.org", "expected_match": "test.user@domain.org", "description": "Email with dot"},
            {"input_string": "Support: help123@company.co.uk", "expected_match": "help123@company.co.uk", "description": "Complex domain"}
        ]

        for case in email_cases:
            test_cases.append(case)

        # Test a comprehensive email regex
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        arguments = {"pattern": email_pattern}

        result = await handle_call_tool("test_regex", arguments)

        assert len(result) == 1
        text = result[0].text
        assert "3 passed, 0 failed" in text
        assert "All test cases passed" in text

if __name__ == "__main__":
    pytest.main([__file__])

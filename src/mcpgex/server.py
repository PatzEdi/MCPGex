import asyncio
import re
from typing import Any, Dict, List, Optional, Tuple
import json

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


# Global storage for test cases
test_cases: List[Dict[str, Any]] = []

# Initialize the MCP server
server = Server("mcpgex")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools for regex pattern testing."""
    return [
        types.Tool(
            name="add_test_case",
            description="Add a test case for regex pattern validation. Each test case consists of an input string and the expected match/output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_string": {
                        "type": "string",
                        "description": "The input string to test the regex pattern against"
                    },
                    "expected_matches": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of substrings that should be matched/extracted by the regex"
                    },
                    "groups": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "The groups that should be extracted by the regex. This is an array of numbers"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of what this test case is checking for"
                    }
                },
                "required": ["input_string", "expected_matches", "groups"]
            }
        ),
        types.Tool(
            name="test_regex",
            description="Test a regex pattern against all current test cases to see if it satisfies the requirements.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The regex pattern to test"
                    },
                    "flags": {
                        "type": "string",
                        "description": "Optional regex flags (e.g., 'i' for case-insensitive, 'm' for multiline, 's' for dotall). Default is no flags.",
                        "default": ""
                    }
                },
                "required": ["pattern"]
            }
        ),
        types.Tool(
            name="get_test_cases",
            description="Get all current test cases to see what requirements the regex pattern needs to satisfy.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="clear_test_cases",
            description="Clear all test cases to start fresh with new requirements.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> List[types.TextContent]:
    """Handle tool calls for regex pattern testing."""

    if name == "add_test_case":
        input_string = arguments.get("input_string", "")
        expected_matches = arguments.get("expected_matches", [])
        groups = arguments.get("groups", [])
        description = arguments.get("description", "")

        if len(groups) != len(expected_matches):
            return [
                types.TextContent(
                    type="text",
                    text=f"Error: Invalid test case. Number of groups ({len(groups)}) does not match number of expected matches ({len(expected_matches)}). Perhaps, input string contains multiple matches?"
                )
            ]

        test_case = {
            "input_string": input_string,
            "expected_matches": expected_matches,
            "groups": groups,
            "description": description
        }

        test_cases.append(test_case)

        return [
            types.TextContent(
                type="text",
                text=f"Added test case:\n- Input: '{input_string}'\n- Expected matches: {expected_matches}\n- Groups: {groups}\n- Description: {description or 'None'}\n\nTotal test cases: {len(test_cases)}"
            )
        ]

    elif name == "test_regex":
        pattern = arguments.get("pattern", "")
        flags_str = arguments.get("flags", "")

        if not test_cases:
            return [
                types.TextContent(
                    type="text",
                    text="No test cases defined. Please add test cases first using add_test_case."
                )
            ]

        # Convert flags string to regex flags
        flags = 0
        if flags_str:
            if 'i' in flags_str.lower():
                flags |= re.IGNORECASE
            if 'm' in flags_str.lower():
                flags |= re.MULTILINE
            if 's' in flags_str.lower():
                flags |= re.DOTALL
            if 'x' in flags_str.lower():
                flags |= re.VERBOSE

        try:
            compiled_pattern = re.compile(pattern, flags)
        except re.error as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"Invalid regex pattern: {e}"
                )
            ]

        results = []
        passed = 0
        failed = 0
        no_match = 0

        results.append(f"Testing regex pattern: {pattern}")
        if flags_str:
            results.append(f"Flags: {flags_str}")
        results.append("-" * 50)

        for i, test_case in enumerate(test_cases, 1):
            input_str = test_case["input_string"]
            groups = test_case["groups"]
            expected_matches = test_case["expected_matches"]
            description = test_case.get("description", "")

            # Try to find the expected match in the input string
            match = compiled_pattern.search(input_str)

            if match:
                # Check if the match contains the expected substring
                matched_texts = [match.group(g) for g in groups] if groups else [match.group(0)] # Where groups  = e.g. [1,2]
                if sorted(matched_texts) == sorted(expected_matches):
                    results.append(f"✅ Test case {i}: PASSED")
                    results.append(f"   Input: '{input_str}'")
                    results.append(f"   Expected: {expected_matches}")
                    results.append(f"   Groups: '{groups}'")
                    results.append(f"   Matched: {matched_texts}")
                    if description:
                        results.append(f"   Description: {description}")
                    passed += 1
                else:
                    results.append(f"🛑 Test case {i}: FAILED")
                    results.append(f"   Input: '{input_str}'")
                    results.append(f"   Expected: '{expected_matches}'")
                    results.append(f"   Groups: '{groups}'")
                    results.append(f"   Matched: '{matched_texts}' (doesn't match expected)")
                    if description:
                        results.append(f"   Description: {description}")
                    failed += 1
            else:
                results.append(f"0️⃣ Test case {i}: NO MATCHES FOUND")
                results.append(f"   Input: '{input_str}'")
                results.append(f"   Expected: '{expected_matches}'")
                results.append(f"   Groups: '{groups}'")
                results.append(f"   Matched: '{[]}'")
                if description:
                    results.append(f"   Description: {description}")
                no_match += 1

            results.append("")

        results.append("-" * 50)
        results.append(f"Summary: {passed} passed, {failed} failed, {no_match} with no match")

        if failed == 0:
            results.append("🎉 All test cases passed! The regex pattern is working correctly.")
        else:
            results.append("💡 Some test cases failed. Consider adjusting the regex pattern.")

        return [
            types.TextContent(
                type="text",
                text="\n".join(results)
            )
        ]

    elif name == "get_test_cases":
        if not test_cases:
            return [
                types.TextContent(
                    type="text",
                    text="No test cases defined yet. Use add_test_case to add requirements for your regex pattern."
                )
            ]

        result = ["Current test cases:"]
        result.append("=" * 40)

        for i, test_case in enumerate(test_cases, 1):
            result.append(f"Test case {i}:")
            result.append(f"  Input: '{test_case['input_string']}'")
            result.append(f"  Expected matches: {test_case['expected_matches']}")
            result.append(f"   Groups: '{test_case['groups']}'")
            if test_case.get("description"):
                result.append(f"  Description: {test_case['description']}")
            result.append("")

        result.append(f"Total: {len(test_cases)} test cases")

        return [
            types.TextContent(
                type="text",
                text="\n".join(result)
            )
        ]

    elif name == "clear_test_cases":
        count = len(test_cases)
        test_cases.clear()

        return [
            types.TextContent(
                type="text",
                text=f"Cleared all test cases. Removed {count} test case(s)."
            )
        ]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def serve():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcpgex",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(serve())

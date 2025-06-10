#!/usr/bin/env python3

"""
Example usage of the Regex MCP Server

This script demonstrates the typical workflow for using the regex MCP server:
1. Define test cases with input strings and expected matches
2. Test different regex patterns until all cases pass
3. Get the final working regex pattern

Note: This is a conceptual example showing the workflow.
In practice, you would interact with the MCP server through an MCP client.
"""

def example_workflow():
    """
    Example workflow for using the Regex MCP server
    """

    print("=== Regex MCP Server Example Workflow ===\n")

    # Step 1: Define what we want our regex to match
    print("Step 1: Define test cases")
    print("Let's say we want to extract email addresses from text.")
    print()

    test_cases = [
        {
            "input_string": "Contact me at john.doe@example.com for more info",
            "expected_match": "john.doe@example.com",
            "description": "Basic email extraction"
        },
        {
            "input_string": "My work email is jane_smith123@company.org",
            "expected_match": "jane_smith123@company.org",
            "description": "Email with underscore and numbers"
        },
        {
            "input_string": "Reach out to support@test-site.co.uk anytime",
            "expected_match": "support@test-site.co.uk",
            "description": "Email with hyphens and country domain"
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"  Input: '{case['input_string']}'")
        print(f"  Expected: '{case['expected_match']}'")
        print(f"  Description: {case['description']}")
        print()

    # Step 2: Try different regex patterns
    print("Step 2: Test regex patterns")
    print()

    patterns_to_try = [
        {
            "pattern": r"\w+@\w+\.\w+",
            "description": "Simple pattern - likely too basic"
        },
        {
            "pattern": r"\w+@\w+\.\w+\.\w+",
            "description": "Pattern for domains with country code - too specific"
        },
        {
            "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "description": "Comprehensive email pattern"
        }
    ]

    for i, pattern_info in enumerate(patterns_to_try, 1):
        print(f"Trying Pattern {i}: {pattern_info['pattern']}")
        print(f"Description: {pattern_info['description']}")

        # Simulate testing each pattern
        import re
        pattern = re.compile(pattern_info['pattern'])

        passed = 0
        failed = 0

        for j, case in enumerate(test_cases, 1):
            match = pattern.search(case['input_string'])
            if match and match.group(0) == case['expected_match']:
                print(f"  ✅ Test case {j}: PASSED")
                passed += 1
            else:
                print(f"  ❌ Test case {j}: FAILED")
                if match:
                    print(f"     Got: '{match.group(0)}', Expected: '{case['expected_match']}'")
                else:
                    print(f"     Got: None, Expected: '{case['expected_match']}'")
                failed += 1

        print(f"  Result: {passed} passed, {failed} failed")

        if failed == 0:
            print(f"  🎉 Perfect! This pattern works for all test cases.")
            print(f"  Final regex: {pattern_info['pattern']}")
            break
        else:
            print(f"  💡 This pattern needs improvement.")

        print()

def mcp_client_commands():
    """
    Show the actual MCP client commands you would use
    """

    print("\n=== MCP Client Commands ===\n")
    print("Here are the actual commands you would use with an MCP client:\n")

    print("1. Add test cases:")
    print('   add_test_case(input_string="Contact me at john.doe@example.com", expected_match="john.doe@example.com")')
    print('   add_test_case(input_string="My work email is jane_smith123@company.org", expected_match="jane_smith123@company.org")')
    print('   add_test_case(input_string="Reach out to support@test-site.co.uk", expected_match="support@test-site.co.uk")')
    print()

    print("2. View current test cases:")
    print('   get_test_cases()')
    print()

    print("3. Test regex patterns:")
    print('   test_regex(pattern=r"\\w+@\\w+\\.\\w+")')
    print('   test_regex(pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")')
    print()

    print("4. Clear test cases when starting fresh:")
    print('   clear_test_cases()')
    print()

def use_cases():
    """
    Show different use cases for the regex MCP server
    """

    print("\n=== Common Use Cases ===\n")

    use_cases = [
        {
            "name": "Email Validation",
            "test_cases": [
                ("user@domain.com", "user@domain.com"),
                ("Contact: admin@site.org", "admin@site.org")
            ]
        },
        {
            "name": "Phone Number Extraction",
            "test_cases": [
                ("Call me at (555) 123-4567", "(555) 123-4567"),
                ("My number is 555-123-4567", "555-123-4567")
            ]
        },
        {
            "name": "URL Extraction",
            "test_cases": [
                ("Visit https://www.example.com for more", "https://www.example.com"),
                ("Check out http://test.org/page", "http://test.org/page")
            ]
        },
        {
            "name": "Date Parsing",
            "test_cases": [
                ("The meeting is on 2024-03-15", "2024-03-15"),
                ("Date: 03/15/2024", "03/15/2024")
            ]
        }
    ]

    for use_case in use_cases:
        print(f"{use_case['name']}:")
        for input_str, expected in use_case['test_cases']:
            print(f"  Input: '{input_str}' → Expected: '{expected}'")
        print()

if __name__ == "__main__":
    example_workflow()
    mcp_client_commands()
    use_cases()

    print("\n=== Getting Started ===")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the server: python server.py")
    print("3. Connect with an MCP client to start testing regex patterns!")

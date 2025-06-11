from .server import serve


def main():
    """ MCPGex - MCP server for finding, testing and refining regex patterns"""
    import asyncio
    asyncio.run(serve())

if __name__ == "__main__":
    main()
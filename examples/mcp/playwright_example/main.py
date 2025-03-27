import asyncio
import glob
import os
import shutil
from datetime import datetime

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio


async def run(mcp_server: MCPServer):
    # Create a directory for screenshots if it doesn't exist
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # agent with enhanced instructions for screenshot capability
    agent = Agent(
        name="Web Screenshot Assistant",
        instructions="""
        You are a web screenshot assistant that follows a Read-Eval-Test (RET) loop pattern:

        Read:
        - Understand the user's request for website navigation and screenshots
        - Identify any specific elements or areas to capture
        - Note any special requirements for the screenshot

        Eval:
        - Choose appropriate Playwright tools for the task
        - Plan the sequence of actions (navigation, waiting, screenshot)
        - Determine the best filename and location for saving

        Test:
        - Verify successful navigation and page load
        - Confirm screenshot capture
        - Report back with results and file locations

        Guidelines:
        - Always wait for page load before screenshots
        - Use page.locator() for specific elements
        - Save to "screenshots" directory with descriptive names
        - Use PNG format for quality
        - Include domain and date in filenames
        - Capture full page content when needed
        """,
        mcp_servers=[mcp_server],
    )

    # Gather the available tools to understand what we can do with Playwright
    tools = await agent.get_all_tools()
    print("Available tools:", [tool.name for tool in tools])

    while True:
        # Read: Get user input
        print("\nEnter your request (or 'exit' to quit):")
        user_request = input().strip()

        if user_request.lower() == 'exit':
            break

        print(f"\nProcessing request: {user_request}\n")

        # Eval: Run the agent with the request
        result = await Runner.run(starting_agent=agent, input=user_request)

        # Test: Display results and verify screenshots
        print("\nResult:", result)

async def main():
    server = None
    try:
        # Configure the MCP server
        # Note: remove --headless if you want to see the browser in action
        server = MCPServerStdio(
            name="Playwright Screenshot Server",
            params={
                "command": "npx",
                "args": ["-y", "@playwright/mcp@latest", "--headless"],
            },
        )
        await server.__aenter__()

        trace_id = gen_trace_id()
        with trace(workflow_name="Playwright Screenshot Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            print(f"Starting Playwright server: {server}")

            # Run our screenshot example
            await run(server)
    finally:
        if server:
            try:
                await server.__aexit__(None, None, None)
            except Exception as e:
                print(f"Warning: Error during server cleanup: {e}")

if __name__ == "__main__":
    asyncio.run(main())

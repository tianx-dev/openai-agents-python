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
        name="Playwright Assistant",
        instructions="""
        You are a playwright assistant that follows a Read-Eval-Test (RET) loop pattern:
        - Read: Understand the user's request for website navigation and screenshots
        - Eval: Choose appropriate Playwright tools for the task
        - Test: Verify successful navigation and page load
        - Report back with results and file locations
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


    # rewrite this with async with
    async with MCPServerStdio(
        name="Playwright Screenshot Server",
        params={
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--headless"],
        },
    ) as server:
        trace_id = gen_trace_id()
        await server.__aenter__()

        trace_id = gen_trace_id()
        with trace(workflow_name="Playwright Screenshot Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            print(f"Starting Playwright server: {server}")

            # Run our screenshot example
            await run(server)

if __name__ == "__main__":
    asyncio.run(main())

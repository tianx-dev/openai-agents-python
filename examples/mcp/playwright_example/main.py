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
        You are a web screenshot assistant that can navigate to websites and capture screenshots.

        Use the Playwright tools to:
        1. Navigate to websites requested by the user
        2. Take screenshots of the entire page or specific elements
        3. Save screenshots with descriptive filenames that include the website name and current date
        4. Report back with the location of saved screenshots

        Follow these guidelines:
        - Always wait for the page to fully load before taking screenshots
        - If asked to capture a specific element, use page.locator() and then screenshot that element
        - If no specific path is provided, save screenshots to the "screenshots" directory
        - Generate descriptive filenames that include the website domain and current date
        - Always confirm successful screenshot capture and provide the filepath where it was saved
        - For full-page screenshots, capture the entire page scrolling content

        When saving screenshots:
        - Use PNG format for better quality
        - Include helpful information in the filename (website, date, element if applicable)
        - Report success with the full path where the screenshot was saved
        """,
        mcp_servers=[mcp_server],
    )

    # Gather the available tools to understand what we can do with Playwright
    tools = await agent.get_all_tools()
    print("Available tools:", [tool.name for tool in tools])

    # Define the default screenshot path with current date
    today_date = datetime.now().strftime("%Y-%m-%d")
    default_screenshot_path = os.path.join(screenshots_dir, f"openai_{today_date}.png")

    # Run the agent with a screenshot task
    user_request = f"""
    Please perform these steps:
    1. Navigate to https://example.com
    2. Wait for the page to fully load
    3. Take a screenshot of the entire page
    4. Save it to {default_screenshot_path}
    5. Then navigate to https://httpbin.org
    6. Take another screenshot with a descriptive filename in the screenshots directory
    """

    print(f"\nProcessing request: {user_request}\n")

    # Run the agent with our request
    result = await Runner.run(starting_agent=agent, input=user_request)

    # Display the result
    print("\nResult:", result)

    # Verify the screenshots were created
    if os.path.exists(default_screenshot_path):
        print(f"\nSuccessfully created primary screenshot at: {default_screenshot_path}")
        # Get the file size
        file_size = os.path.getsize(default_screenshot_path) / 1024  # KB
        print(f"Screenshot size: {file_size:.2f} KB")

    # List all screenshots created
    all_screenshots = glob.glob(os.path.join(screenshots_dir, "*.png"))
    print(f"\nAll screenshots in directory ({len(all_screenshots)}):")
    for screenshot in all_screenshots:
        file_size = os.path.getsize(screenshot) / 1024  # KB
        print(f" - {os.path.basename(screenshot)} ({file_size:.2f} KB)")


async def main():
    # Configure the MCP server
    # Note: remove --headless if you want to see the browser in action
    async with MCPServerStdio(
        name="Playwright Screenshot Server",
        params={
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--headless"],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Playwright Screenshot Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            print(f"Starting Playwright server: {server}")

            # Run our screenshot example
            await run(server)


if __name__ == "__main__":
    asyncio.run(main())

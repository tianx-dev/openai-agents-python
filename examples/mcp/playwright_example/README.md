# Playwright Screenshot Example

This example demonstrates how to use the OpenAI Agents SDK with Playwright MCP (Machine Control Protocol) to automate browser interactions and capture screenshots.

## Features

- Navigates to websites
- Captures full-page screenshots
- Saves screenshots with descriptive filenames
- Reports file information

## Requirements

- Node.js and npm
- Python 3.9+ with the OpenAI Agents SDK installed

## Installation

Before running this example, make sure you have the Playwright MCP package available:

```bash
# This will be installed automatically when you run the example
npm install -g @playwright/mcp
```

## Usage

Run the example:

```bash
python main.py
```

The script will:
1. Launch a headless Playwright browser via the MCP server
2. Navigate to OpenAI's website
3. Capture screenshots
4. Save them to the `screenshots` directory

## Customization

- Modify `user_request` in `main.py` to capture different websites
- Remove the `--headless` flag in the MCP server configuration to see the browser in action
- Extend the agent's instructions to handle more complex browser automation tasks

## Additional Capabilities

This example only demonstrates basic screenshot functionality, but the Playwright MCP server can be used for:

- Form filling and submission
- Web scraping
- UI testing
- Authentication flows
- And much more!

For more information on Playwright capabilities, see the [Playwright documentation](https://playwright.dev/docs/intro).
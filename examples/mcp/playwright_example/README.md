# Playwright Screenshot Example

This example uses the [Playwright MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright), running locally via `npx`.

Run it via:

```bash
uv run python examples/mcp/playwright_example/main.py
```

## Details

The example uses the `MCPServerStdio` class from `agents.mcp`, with the command:

```bash
npx -y "@playwright/mcp@latest" --headless
```

The script demonstrates browser automation capabilities by:
1. Navigating to example.com and httpbin.org
2. Taking full-page screenshots
3. Saving them to a local `screenshots` directory with descriptive filenames

Under the hood:

1. The server is spun up in a subprocess, and exposes Playwright tools for browser automation
2. We add the server instance to the Agent via `mcp_servers`
3. Each time the agent runs, we call out to the MCP server to fetch the list of tools via `server.list_tools()`
4. If the LLM chooses to use an MCP tool, we call the MCP server to run the tool via `server.run_tool()`

## RET Loop

The example demonstrates a Read-Eval-Test loop:

1. **Read**: The agent reads the user's request to navigate to websites and take screenshots
2. **Eval**: The agent evaluates which Playwright tools to use (navigation, screenshot capture)
3. **Test**: The agent tests the results by:
   - Verifying successful navigation
   - Confirming screenshot capture
   - Checking file sizes and locations

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
## Concept of MCP

**What MCP is NOT doing**

It's not translating API responses into natural language prompts. The raw data from your tools (JSON, numbers, strings) goes back as-is.

**What MCP IS doing**

It's acting as a **capability registry + standardized communication bridge** between your code and any LLM host.

**What happens at runtime**

1. LLM host asks the MCP server: *"what tools do you have?"*
2. MCP server responds with the tool names, descriptions, and input schemas (it reads these from your `@mcp.tool` decorators + docstrings)
3. LLM decides to call `get_share_price(ticker="AAPL")`
4. MCP server executes your function, gets back `{"price": 189.34}`
5. That raw result goes back to the LLM as a **tool result message** in the conversation
6. The LLM then reasons over it and produces a response to the user

**Step 2 is the critical one** — your docstrings and type hints on the decorated functions become the "API contract" the LLM reads to decide *when and how* to call your tool. That's why good docstrings matter more in MCP than in regular code.
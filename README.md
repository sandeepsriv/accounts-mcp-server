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

**Analogy refined**

> *"inserting MCP is like publishing your internal functions as a discoverable, standardized API that any LLM host can introspect and call without you writing any glue code."*
> 

The MCP server isn't translating — it's **exposing** and **routing**.

**You're right that REST + JSON works.** OpenAI's function calling already does exactly what you described — you define a JSON schema for your function, the LLM calls your REST endpoint, gets JSON back, reasons over it. That's been working for years.

---

**So where does MCP actually add value?**

**1. Discovery at runtime**

With REST, you still have to *tell* the LLM about your API — hardcoded function schemas in a system prompt, or a config file. The LLM doesn't discover it dynamically.

With MCP, the host connects and asks *"what tools do you have?"* and gets back schemas automatically. No manual registration per host.

**2. stdio transport — no HTTP server needed**

This is the practical win for local dev tools. Claude Code, Cursor, etc. don't want to hit a hosted HTTP endpoint for local file operations. MCP over `stdio` means your tool runs as a local process — no port, no server, no auth headers.

**3. One integration, every host**

With REST + function calling, the schema format differs between OpenAI, Anthropic, Gemini. You write three versions. MCP is one spec that any compliant host speaks.

**4. Resources and Prompts**

MCP isn't just tools — it also standardizes serving *file contents, database rows, documents* (Resources) and reusable *prompt templates* (Prompts) to the host. REST has no equivalent convention for this

**MCP is not replacing REST. It's a thin standardization layer *on top of* the same JSON concepts, specifically designed for the LLM tool-calling workflow.** If you're only ever connecting to one LLM host and don't need local stdio tools, a plain REST API with function calling schemas gets you 80% there.
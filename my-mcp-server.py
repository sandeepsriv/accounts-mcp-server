import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from accounts import Account

load_dotenv(override=True)

account = Account.get("sandeep")

params = {
    "command": "uv",
    "args": ["run", "accounts_server.py"]
}

instructions = "You are able to manage an account for a client, and answer questions about the account."
request = "My name is Sandeep and my account is under the name sandeep. What's my balance and my holdings?"
model = "gpt-4.1-mini"

async def main():
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = Agent(name="account_manager", instructions=instructions, model=model, mcp_servers=[mcp_server])
        with trace("account_manager"):
            result = await Runner.run(agent, request)
        print(result.final_output)

asyncio.run(main())
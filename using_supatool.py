from typing import Any, Dict
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
from supatoolkit import Supatoolkit
from langchain_openai import ChatOpenAI
import requests

supatool_kit = Supatoolkit()
supatool = supatool_kit.get_tools()

llm = ChatOpenAI(temperature=0, model="gpt-4")


@tool
def determine_tool(query: str) -> Dict[str, Any]:
    """
    Determines the optimal tool to use based on the user query.
    """
    TOOL_SELECTOR_API = "http://localhost:5002/get_tool"
    response = requests.post(TOOL_SELECTOR_API, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to determine the tool"}


@tool
def execute_tool(endpoint: str, args) -> Dict[str, Any]:
    """
    Executes the tool based on the endpoint and arguments.
    Determine the correct arguments to pass to the tool based on the tool's description.
    """
    response = requests.post(endpoint, json=args)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Tool execution failed"}


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a powerful assistant. Always use the provided tools to answer queries. First, determine the tool, then generate the necessary arguments, and finally execute the tool."
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [determine_tool, execute_tool]


llm_with_tools = llm.bind_tools(tools)


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def main():
    user_input = input("Enter your query: ")
    list(agent_executor.stream({"input": user_input}))


if __name__ == "__main__":
    main()

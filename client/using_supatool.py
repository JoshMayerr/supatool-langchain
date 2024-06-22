from typing import Any, Dict
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool
from langchain_openai import ChatOpenAI
import requests

from toolkit.supatoolkit import SupaToolkit


llm = ChatOpenAI(temperature=0, model="gpt-4")
llm_with_tools = llm.bind_tools(SupaToolkit().get_tools())

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a powerful assistant. Always use the provided tools to answer queries. Determine the optimal tool using supa_search, then execute the tool using supa_execute with the corresponding endpoint and args. Only use these two tools."
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

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


agent_executor = AgentExecutor(
    agent=agent, tools=SupaToolkit().get_tools(), verbose=True)


def main():
    # user_input = input("Enter your query: ")
    list(agent_executor.stream({"input": "weather in boston"}))


if __name__ == "__main__":
    main()

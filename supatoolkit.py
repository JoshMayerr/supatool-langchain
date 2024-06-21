from typing import Dict, List
from langchain_core.tools import BaseToolkit
from langchain_community.tools import BaseTool
import requests
from supatool import Supatool


class Supatoolkit(BaseToolkit):
    tools: List[BaseTool] = [Supatool()]

    def get_tools(self) -> List[BaseTool]:
        return self.tools


class SupatoolSearch(BaseTool):
    name: str = "supatool_search"
    endpoint: str = "http://localhost:5002/get_tool"
    description: str = "A tool that searches for the optimal tool to use based on the user query."

    def _run(self, query: str) -> Dict:
        response = requests.post(self.endpoint, json={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to determine the tool"}


class SupatoolExecute(BaseTool):
    name: str = "supatool_execute"
    description: str = "A tool that executes the optimal tool based on the user query."

    def _run(self, endpoint: str, args: Dict) -> Dict:
        response = requests.post(endpoint, json=args)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Tool execution failed"}

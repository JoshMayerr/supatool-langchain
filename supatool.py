from langchain_community.tools import BaseTool
import requests
from typing import Dict


class Supatool(BaseTool):
    name: str = "supatool"
    description: str = "A generic tool that will wrap all Supatool System Actions"
    search_endpoint: str = "http://localhost:5002/get_tool"

    def generate_args(self, args_description):
        if args_description is None:
            return {}
        args = {}
        for arg, arg_type in args_description.items():
            user_input = input(f"Please provide the {arg} ({arg_type}): ")
            args[arg] = user_input
        return args

    def determine_tool(self, query):
        response = requests.post(self.search_endpoint, json={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to determine the tool"}

    def execute_tool(self, endpoint, args):
        response = requests.post(endpoint, json=args)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Tool execution failed"}

    def _run(self, query: str) -> Dict:
        tool_info = self.determine_tool(query)
        print(tool_info)
        if "error" in tool_info:
            return tool_info

        endpoint = tool_info.get("endpoint")
        args_description = tool_info.get("arg")
        args = self.generate_args(args_description)

        result = self.execute_tool(endpoint, args)
        return result

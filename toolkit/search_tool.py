from typing import Any, Dict, Type
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel
import requests


class SearchToolArgs(BaseModel):
    query: str


class SupaSearchTool(BaseTool):
    name: str = "supa_search"
    description: str = "A tool that searches for the optimal tool to use based on the user query."
    args_schema: Type[BaseModel] = SearchToolArgs
    return_direct: bool = False
    handle_tool_error: bool = True
    TOOL_SELECTOR_API = "http://localhost:5002/get_tool"

    def _run(self, query: str):
        return self._search_for_tool(query)

    def _search_for_tool(self, query: str) -> Dict[str, Any]:
        """
        Determines the optimal tool to use based on the user query.
        """
        response = requests.post(self.TOOL_SELECTOR_API, json={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            raise ToolException(
                "Unable to find an optimal tool for the query.")

from typing import Any, Dict, Type
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field
import requests


class ExecuteToolArgs(BaseModel):
    endpoint: str = Field(description="The API endpoint to execute the tool.")
    args: Dict[str, Any] = Field(
        description="The arguments to pass to the tool. The arguments should be based on the tool's description and the user's query.")


class SupaExecuteTool(BaseTool):
    name: str = "supa_execute"
    description: str = "Executes a tool based on the endpoint and arguments. Determine the correct arguments to use based on the tool's description."
    handle_tool_error: bool = True
    args_schema: Type[BaseModel] = ExecuteToolArgs

    def _run(self, endpoint: str, args: Dict[str, Any]):
        return self._execute_tool(endpoint, args)

    def _execute_tool(self, endpoint: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the tool based on the endpoint and arguments.
        Determine the correct arguments to pass to the tool
        based on the tool's description.
        """
        response = requests.post(endpoint, json=args)
        if response.status_code == 200:
            return response.json()
        else:
            raise ToolException("Tool execution failed.")

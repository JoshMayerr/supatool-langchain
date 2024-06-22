from typing import Any, Dict, List, Type
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field
import requests


class InputParameter(BaseModel):
    llm_name: str
    description: str
    type: str
    query_key: str


class Metadata(BaseModel):
    name: str
    endpoint: str = Field(description="The API endpoint to execute the tool.")
    method: str
    inputParams: List[InputParameter] = Field(
        "Input params and their keys for the API endpoint")


class ExecuteToolArgs(BaseModel):
    metadata: Metadata = Field(
        description="The metadata of the tool to execute. Copy this exactly from supa_search.")
    args: Dict[str, Any] = Field(
        description="The arguments to pass to the tool. The arguments should be based on the tool's description and the user's query.")


class SupaExecuteTool(BaseTool):
    name: str = "supa_execute"
    description: str = "Executes a tool based on the endpoint and arguments. Determine the correct arguments to use based on the tool's description."
    handle_tool_error: bool = True
    args_schema: Type[BaseModel] = ExecuteToolArgs

    def _run(self,  metadata: Metadata, args: Dict[str, Any]):
        return self._execute_tool(metadata, args)

    def _execute_tool(self,  metadata: Metadata, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the tool based on the endpoint and arguments.
        Determine the correct arguments to pass to the tool
        based on the tool's description.
        """
        print(metadata, args)
        args = self._match_input_params(metadata, args)
        args["key"] = "1bf5a3b415e44dff984181153242105"
        if metadata.method == "GET":
            response = requests.get(
                metadata.endpoint, params=args)
        else:
            response = requests.post(metadata.endpoint, json=args)
        if response.status_code == 200:
            return response.json()
        else:
            print(response)
            raise ToolException("Tool execution failed.")

    def _match_input_params(self, metadata: Metadata, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match the input params from the metadata to the args.
        """
        matched_args = {}
        for input_param in metadata.inputParams:
            if input_param.llm_name in args:
                matched_args[input_param.query_key] = args[input_param.llm_name]
        return matched_args

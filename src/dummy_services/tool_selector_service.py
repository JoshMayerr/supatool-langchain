"""
A test implementation that selects the optimal tool to use based on an end user query.
"""

from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Query(BaseModel):
    query: str


class InputParameter(BaseModel):
    llm_name: str
    description: str
    type: str
    query_key: str


class Metadata(BaseModel):
    name: str
    endpoint: str
    method: str
    inputParams: List[InputParameter]


class ToolResponse(BaseModel):
    metadata: Metadata
    args: dict


@app.post("/get_tool", response_model=ToolResponse)
def get_tool(query: Query):
    """
    @param query: The user query

    Return the optimal tool to use based on the user query.
    """

    query_str = query.query.lower()

    if "weather" in query_str:

        meta = Metadata(
            inputParams=[InputParameter(
                llm_name="location", description="The location to get the weather for", type="string", query_key="q")],
            name="get_weather", endpoint="https://api.weatherapi.com/v1/forecast.json", method="GET")

        args_description = {"location": "string"}

    elif "flight" in query_str:
        args_description = {
            "destination": "string",
            "date": "string"
        }
        meta = Metadata(
            name="search_flights", endpoint="http://localhost:5001/search_flights", method="POST")
    elif "hotel" in query_str:
        args_description = {
            "destination": "string",
            "checkin_date": "string",
            "checkout_date": "string"
        }
        meta = Metadata(
            name="check_hotels", endpoint="http://localhost:5001/check_hotels", method="POST")
    elif "hello" in query_str:
        args_description = {}
        meta = Metadata(
            name="say_hello", endpoint="http://localhost:5001/say_hello", method="POST")
    else:
        raise HTTPException(status_code=400, detail="No suitable tool found")

    print(ToolResponse(metadata=meta, args=args_description))
    return ToolResponse(metadata=meta, args=args_description)


uvicorn.run(app, host="0.0.0.0", port=5002)

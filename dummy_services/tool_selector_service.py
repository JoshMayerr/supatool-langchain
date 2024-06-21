"""
A test implementation that selects the optimal tool to use based on an end user query.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Query(BaseModel):
    query: str


class ToolResponse(BaseModel):
    tool: str
    endpoint: str
    args: dict


@app.post("/get_tool", response_model=ToolResponse)
def get_tool(query: Query):
    """
    @param query: The user query

    Return the optimal tool to use based on the user query.
    """

    query_str = query.query.lower()
    print(query_str)

    if "weather" in query_str:
        tool = "get_weather"
        endpoint = "http://localhost:5001/get_weather"
        args_description = {"destination": "string"}
    elif "flight" in query_str:
        tool = "search_flights"
        endpoint = "http://localhost:5001/search_flights"
        args_description = {
            "destination": "string",
            "date": "string"
        }
    elif "hotel" in query_str:
        tool = "check_hotels"
        endpoint = "http://localhost:5001/check_hotels"
        args_description = {
            "destination": "string",
            "checkin_date": "string",
            "checkout_date": "string"
        }
    elif "hello" in query_str:
        tool = "say_hello"
        endpoint = "http://localhost:5001/say_hello"
        args_description = {}
    else:
        raise HTTPException(status_code=400, detail="No suitable tool found")

    return ToolResponse(tool=tool, endpoint=endpoint, args=args_description)


uvicorn.run(app, host="0.0.0.0", port=5002)

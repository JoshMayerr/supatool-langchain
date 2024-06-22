"""
A dummy service that represents all the tools running on the web today.

The endpoints of the tools endpoints :)
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class WeatherRequest(BaseModel):
    destination: str


class FlightsRequest(BaseModel):
    destination: str
    date: str


class HotelsRequest(BaseModel):
    destination: str
    checkin_date: str
    checkout_date: str


@app.post("/get_weather")
def get_weather(request: WeatherRequest):
    # Dummy implementation
    return {"weather": f"Weather in {request.destination} is sunny"}


@app.post("/search_flights")
def search_flights(request: FlightsRequest):
    # Dummy implementation
    return {"flights": [f"Flight to {request.destination} on {request.date}"]}


@app.post("/check_hotels")
def check_hotels(request: HotelsRequest):
    # Dummy implementation
    return {"hotels": [f"Hotel in {request.destination} from {request.checkin_date} to {request.checkout_date}"]}


@app.post("/say_hello")
def say_hello():
    return {"message": "hello world! welcome to supatool"}


uvicorn.run(app, host="0.0.0.0", port=5001)

from pydantic import BaseModel, Field
from typing import Any
from agents import FunctionTool, function_tool
import python_weather

class WeatherToolArgs(BaseModel):
    """
    Pydantic Model for the tool input.

    Parameters:
    location (str): Location of the place to check the weather
    weather_date (date): Date to check the weather
    """

    location: str = Field(..., description="Location")
    weather_date: str = Field(..., description="Date")


@function_tool
async def WeatherTool(args: WeatherToolArgs) -> str:
    """
    Calls a weather API to check the weather
    
    Parameters:
    args (WeatherToolArgs): An instance of WeatherToolArgs.
    Returns:
    str: The weather report on the given location and date
    """

    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(args.location)   # Fetch a weather forecast from a city

        # Get the forecast for the next days also
        forecast = []
        for daily in weather:
            forecast.append(daily)
    
    return f"""The temperature on {args.weather_date} will be {weather.temperature}. This is the forecast for the next days: {forecast}"""

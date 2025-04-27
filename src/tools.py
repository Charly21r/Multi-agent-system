from pydantic import BaseModel
from typing import Any
from agents import FunctionTool, RunContextWrapper
from datetime import date

class WeatherToolArgs(BaseModel):
    """
    Pydantic Model for the tool input.

    Parameters:
    location (str): Location of the place to check the weather
    weather_date (date): Date to check the weather
    """
    location: str
    weather_date: date


def check_weather(args: WeatherToolArgs) -> str:
    """
    Calls a weather API to check the weather
    
    Parameters:
    args (WeatherToolArgs): An instance of WeatherToolArgs.

    Returns:
    str: The weather on the given location and date
    """
    # parsed = WeatherToolArgs.model_validate_json(args)
    
    #TODO: Implement weather api calling
    return f"""The weather will be sunny and amazing, with a little rain on Turedat"""
    # return f"""The weather will be amazing in {parsed.location} on the {parsed.weather_date}"""



WeatherTool = FunctionTool(
    name="check_weather",
    description="Checks weather for a given location and date",
    params_json_schema=WeatherToolArgs.model_json_schema(),
    on_invoke_tool=check_weather,
)
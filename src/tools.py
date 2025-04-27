from pydantic import BaseModel, Field
from typing import Any
from agents import FunctionTool, function_tool

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
def WeatherTool(location: WeatherToolArgs) -> str:
    """
    Calls a weather API to check the weather
    
    Parameters:
    args (WeatherToolArgs): An instance of WeatherToolArgs.
    Returns:
    str: The weather on the given location and date
    """
    # parsed = WeatherToolArgs.model_validate_json(args)
    
    #TODO: Implement weather api calling
    return f"""The weather will be sunny and amazing, with a little rain on Tuesday"""


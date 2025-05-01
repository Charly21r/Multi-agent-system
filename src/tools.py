from pydantic import BaseModel, Field
from agents import function_tool
import python_weather
from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration of the amadeus api client
amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY'),
    client_secret=os.getenv('AMADEUS_API_SECRET')
)


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
    Checks the weather on a given location and day, 
    also includes forecast for the next 3 days.
    
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


class FlightSearchArgs(BaseModel):
    """
    Pydantic Model for the Flight Search Tool input.

    Parameters:
    origin (str): IATA code for the origin location.
    destination (str): IATA code for the destination.
    departure_date (str): date of departure in 'YYYY-MM-DD' format
    num_passengers (int): number of passengers
    """
    origin: str = Field(..., description="IATA code for the origin location")
    destination: str = Field(..., description="IATA code for the destination")
    departure_date: str = Field(..., description="Departure date in 'YYYY-MM-DD' format")
    num_passengers: int = Field(..., description="Number of passengers")


@function_tool
def FlightSearchTool(args: FlightSearchArgs):
    """
    Checks available flights between a given origin and destination for a given date.

    Parameters:
    args (FlightSearchArgs): An instance of FlightSearchArgs
    Returns:
    str: Available flights for the chosen date and route
    """
    try:
        print(args.origin, args.destination, args.departure_date, args.num_passengers)
        # Call the API
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=args.origin,
            destinationLocationCode=args.destination,
            departureDate=args.departure_date,
            adults=args.num_passengers,
            max=5
        )
        
        # Saving the results
        results = []
        for offer in response.data:
            price = offer['price']['total']
            currency = offer['price']['currency']
            itinerary = offer['itineraries'][0]
            segments = itinerary['segments']
            first_segment = segments[0]
            last_segment = segments[-1]

            flight_info = {
                "price": f"{price} {currency}",
                "departure_airport": first_segment['departure']['iataCode'],
                "departure_time": first_segment['departure']['at'],
                "arrival_airport": last_segment['arrival']['iataCode'],
                "arrival_time": last_segment['arrival']['at'],
                "airline": first_segment['carrierCode'],
                "duration": itinerary['duration']
            }

            results.append(flight_info)

        return results
    except ResponseError as error:
        
        print(error)
        return None

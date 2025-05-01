import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from tools import WeatherTool, FlightSearchTool

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')  # OpenAI API Key configuration


# Load agent prompts from the files
try:
    with open('./prompts/main_agent_prompt.txt', "rb") as f:
        main_agent_prompt = f.read().decode('utf-8')
    with open('./prompts/weather_agent_prompt.txt', "rb") as f:
        weather_agent_prompt = f.read().decode('utf-8')
    with open('./prompts/flight_agent_prompt.txt', "rb") as f:
        flight_agent_prompt = f.read().decode('utf-8')
except Exception as e:
    raise Exception(f"""An exception occurred while loading the system prompt: {e}""")


# Model settings for the main agent
main_agent_settings = ModelSettings(
    parallel_tool_calls=True,   # Allow parallel calls to the tools
    temperature=0.5,
    top_p=0.35
)

# Model settings for the weather agent
weather_agent_settings = ModelSettings(
    parallel_tool_calls=False,   # Disallow parallel calls to the tools
    temperature=0.5,
    top_p=0.35
)

# Model settings for the flights agent
flight_agent_settings = ModelSettings(
    parallel_tool_calls=True,   # Allow parallel calls to the tools
    temperature=0.5,
    top_p=0.35
)


weather_agent = Agent(
    name="Weather Agent",
    model_settings=weather_agent_settings,
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n{weather_agent_prompt}""",
    model="gpt-4o-mini",
    handoff_description="An agent capable of getting realtime weather data",
    tools=[WeatherTool]
)


flight_agent = Agent(
    name="Flight Agent",
    model_settings=flight_agent_settings,
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n{flight_agent_prompt}""",
    model="gpt-4o-mini",
    handoff_description="An agent capable of searching for flights",
    tools=[FlightSearchTool]
)


main_agent = Agent(
    name="Main Agent",
    model_settings=main_agent_settings,
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n{main_agent_prompt}""",
    model="gpt-4o-mini",
    handoffs=[weather_agent, flight_agent]
)


async def main():
    answer = await Runner.run(main_agent, input="Check flights from Madrid to Paris on the 25th of june of 2025")
    print(answer.final_output)


if __name__=="__main__":
    asyncio.run(main())


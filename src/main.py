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
    tools = [
        weather_agent.as_tool(
            tool_name="weather_report",
            tool_description="An agent capable of getting realtime weather data"
        ),
        flight_agent.as_tool(
            tool_name="flight_search",
            tool_description="An agent capable of searching for flights"
        )
    ]
)



async def run_agent(query:str):
    """
    
    """
    answer = await Runner.run(main_agent, input=user_message)
    return answer.final_output


def display_history():
    """

    """
    for message in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(message["User"])
        with st.chat_message("assistant"):
            st.markdown(message["Agent"])


if __name__=="__main__":
    # Set title for the streamlit UI
    st.title("Trip Planning Agent")

    # Add message history to the session state
    if "history" not in st.session_state:
        st.session_state["history"] = []
    
    display_history()

    user_message = st.chat_input("Enter your message")   # User's input

    if user_message:
        # Display user message on the screen
        with st.chat_message("user"):
            st.markdown(user_message)
        answer = asyncio.run(run_agent(user_message))
        st.session_state.history.append({"User": user_message, "Agent": answer})    # Add message and response to the history


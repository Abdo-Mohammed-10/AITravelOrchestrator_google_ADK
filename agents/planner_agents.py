from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from System_travel.tools.weather_api import get_weather
import os
model = LiteLlm(
    model="openrouter/openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_weather_for_destination(destination: str) -> dict:
    """Fetch weather data using the weather tool."""
    return get_weather(destination)

planner_agent = Agent(
    name="planner_agent",
    model=model,
    description="Creates structured travel plans that also include destination weather information.",
    instruction=(
        "You are a travel planner. Generate a structured plan (in JSON format) that includes:\n"
        "- destination\n"
        "- duration\n"
        "- activities\n"
        "- estimated_budget\n"
        "- local_tips\n"
        "- current_weather (fetch from weather agent)\n"
        "Always include weather info for the destination before finalizing the plan."
    ),
    tools=[get_weather_for_destination],
)

from google.adk.agents import Agent
from System_travel.tools.weather_api import get_weather
from google.adk.models.lite_llm import LiteLlm
import os

model = LiteLlm(
    model="openrouter/openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

weather_agent = Agent(
    name="weather_agent",
    model=model,
    description="Provides current weather information for a given city.",
    instruction="Use the get_weather tool to fetch and summarize the weather for a city.",
    tools=[get_weather]
)

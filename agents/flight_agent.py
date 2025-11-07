from google.adk.agents import Agent
from System_travel.tools.flight_api import search_flights
from google.adk.models.lite_llm import LiteLlm
import os  

model = LiteLlm(
    model="openrouter/openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

flight_agent = Agent(
    name="flight_agent",
    model=model,
    description="Finds mock flights between origin and destination using an internal Fake Aviation API (for testing).",
    instruction="Use the search_flights tool to return flight offers when the user requests flights. "
                "Parameters: departure_iata (str), arrival_iata (str), date (str, optional). "
                "Return the result from the tool directly.",
    tools=[search_flights],
)

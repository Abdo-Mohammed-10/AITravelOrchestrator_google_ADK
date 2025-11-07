from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from .agents.weather_agent import weather_agent
from .agents.flight_agent import flight_agent
from .agents.planner_agents import planner_agent
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm
import asyncio
import os  

APP_NAME = "Cognitive Resort Planner"

model = LiteLlm(
    model="openrouter/openai/gpt-3.5-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

session_service = InMemorySessionService()
memory =InMemoryMemoryService()

root_agent = Agent(
    name="root_agent",
    model=model,
    sub_agents=[weather_agent, flight_agent, planner_agent],
    description="Routes user prompts to the most suitable sub-agent based on context.",
)



runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service= memory
)

async def main():
    session = await session_service.get_session(APP_NAME, USER_ID, SESSION_ID)
    if session is None:
        session = await session_service.create_session(APP_NAME, USER_ID, SESSION_ID)

    print("Welcome to Cognitive Resort Planner!")
    print("Type your prompt (or 'exit' to quit):\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        from google.genai.types import Content, Part
        user_content = Content(role="user", parts=[Part(text=user_input)])
        final_response = "No response"

        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=user_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text

        print(f"Planner: {final_response}\n")


if __name__ == "__main__":
    asyncio.run(main())
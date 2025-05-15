from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from app.homie.agent import root_agent

# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "homie_assistant"
USER_ID = "default_user"  # In a real app, this would be dynamic per user
SESSION_ID = "default_session"  # In a real app, this would be dynamic per session

# Create the specific session where the conversation will happen
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=root_agent,  # The agent we want to run
    app_name=APP_NAME,  # Associates runs with our app
    session_service=session_service  # Uses our session manager
)
print(f"Runner created for agent '{runner.agent.name}'.")

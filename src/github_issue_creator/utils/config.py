from dotenv import load_dotenv
from beeai_framework.adapters.agentstack.backend.chat import AgentStackChatModel

load_dotenv()

llm = AgentStackChatModel(preferred_models=["openai:gpt-4o"])

# Import after load_dotenv to ensure env vars are loaded
from github_issue_creator.tools.session_manager import SessionManager

# Shared singleton instance
session_manager = SessionManager()

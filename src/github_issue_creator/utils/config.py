import os
from beeai_framework.backend import ChatModel
from dotenv import load_dotenv

from beeai_framework.adapters.agentstack.backend.chat import AgentStackChatModel

load_dotenv()


if os.getenv("API_KEY") is not None:
    print("Using API key from environment variable")
    model = os.getenv("MODEL", "openai:gpt-5-mini")
    llm = ChatModel.from_name(model, {"api_key": os.getenv("API_KEY")})
else:
    print("Using LLM from Agent Stack")
    model = os.getenv("MODEL", "openai:gpt-4o")
    llm = AgentStackChatModel(preferred_models=["openai:gpt-4o"])

# Import after load_dotenv to ensure env vars are loaded
from github_issue_creator.tools.session_manager import SessionManager

# Shared singleton instance
session_manager = SessionManager()

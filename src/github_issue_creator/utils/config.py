import os
from beeai_framework.backend import ChatModel
from dotenv import load_dotenv

from beeai_framework.adapters.agentstack.backend.chat import AgentStackChatModel

load_dotenv()

default_model = "openai:gpt-5-mini"

if os.getenv("API_KEY") is not None:
    model = os.getenv("MODEL", default_model)
    llm = ChatModel.from_name(model, {"api_key": os.getenv("API_KEY")})
else:
    llm = AgentStackChatModel(preferred_models=[default_model])

# Import after load_dotenv to ensure env vars are loaded
from github_issue_creator.tools.session_manager import SessionManager

# Shared singleton instance
session_manager = SessionManager()

from beeai_framework.agents.requirement import RequirementAgent
from github_issue_creator.utils.config import llm


def get_build_mock():
    return RequirementAgent(llm=llm)
import os

import asyncio
from textwrap import dedent

from a2a.types import AgentSkill
from beeai_framework.adapters.beeai_platform.serve.server import BeeAIPlatformServer
from agentstack_sdk.a2a.extensions.ui.agent_detail import AgentDetail, EnvVar
from openinference.instrumentation.beeai import BeeAIInstrumentor

from github_issue_creator.agents.manager import get_agent_manager
from github_issue_creator.agents._build_mock import get_build_mock

BeeAIInstrumentor().instrument()

async def get_root_agent():
    return get_build_mock() if os.getenv("IS_BUILD_PASS") == "true" else await get_agent_manager()

async def run():
    root_agent = await get_root_agent()

    server = BeeAIPlatformServer(config={"configure_telemetry": True, "port": 8000,"host": "0.0.0.0"})
    server.register(
        root_agent,
        name="GitHub Issue Creator",
        description=dedent(
            """\
            Creates well-structured, actionable GitHub issues from user descriptions of bugs or feature requests.
            Uses project documentation and templates to ensure consistency and completeness.
            """
        ),
        default_input_modes=["text"],
        default_output_modes=["text"],
        detail=AgentDetail(
            interaction_mode="multi-turn",
            framework="BeeAI",
            variables=[
                EnvVar(name="GITHUB_REPOSITORY", description="The repository to create the issue in", required=True),
                EnvVar(name="GITHUB_PAT", description="The GitHub Personal Access Token to use for the API", required=True),

                EnvVar(name="DOCS_URL", description="The URL of the documentation to use for the API", required=False),
                EnvVar(name="TEMPLATE_BUG_URL", description="The URL of the bug template to use for the API", required=False),
                EnvVar(name="TEMPLATE_FEATURE_URL", description="The URL of the feature template to use for the API", required=False),
            ],
        ),
        skills=[
            AgentSkill(
                id="create_github_issue",
                name="Create GitHub Issue",
                description=dedent(
                    """\
                    Creates well-structured, actionable GitHub issues from user descriptions of bugs or feature requests.
                    Uses project documentation and templates to ensure consistency and completeness.
                    """
                ),
                tags=["GitHub", "Issues", "Bug Reports", "Feature Requests", "Documentation"],
                examples=[
                    "The login form crashes when I enter special characters in the password field",
                    "Add support for dark mode theme in the user interface",
                    "API returns 500 error when making concurrent requests to /users endpoint",
                    "Implement user authentication with OAuth2 integration",
                    "Memory leak occurs after running the application for several hours",
                ],
            )
        ],
    )
    await server.aserve()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()

import re

from beeai_framework.agents import BaseAgent
from beeai_framework.context import RunContext, RunMiddlewareProtocol
from beeai_framework.emitter import EmitterOptions, EventMeta
from beeai_framework.agents.requirement.events import RequirementAgentFinalAnswerEvent

from github_issue_creator.tools.artifact_handoff import ArtifactStore


class ArtifactMiddleware(RunMiddlewareProtocol):
    """Middleware that expands artifact references in final answers"""

    def __init__(self, artifact_store: ArtifactStore) -> None:
        self._artifact_store = artifact_store

    def bind(self, run: RunContext) -> None:
        agent = run.instance
        assert isinstance(agent, BaseAgent), "Input must be an agent"

        run.emitter.on(
            "final_answer",
            self._handle_final_answer,
            EmitterOptions(match_nested=True, is_blocking=True, priority=2),
        )

    async def _handle_final_answer(self, data: RequirementAgentFinalAnswerEvent, meta: EventMeta) -> None:
        data.delta = self._expand_artifacts(data.delta)

    def _expand_artifacts(self, text: str) -> str:
        """Replace artifact references with full content"""
        # Pattern matches: <artifact id="draft_k3x9" /> or <artifact id="draft_k3x9" summary="..." />
        pattern = r'<artifact\s+id="([^"]+)"(?:\s+summary="[^"]*")?\s*/>'

        def replace_artifact(match):
            artifact_id = match.group(1)
            artifact_data = self._artifact_store.get(artifact_id)
            return artifact_data["content"] if artifact_data else match.group(0)

        return re.sub(pattern, replace_artifact, text)

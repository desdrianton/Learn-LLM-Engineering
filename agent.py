from typing import *

from llm_connector import LLMConnector

# ======================================================================================================================
# Agent (Abstract)
# ======================================================================================================================
class Agent:
    _llm_connector: LLMConnector
    _params: Dict[str, Any]

    def __init__(self, llm_connector: LLMConnector):
        self._llm_connector = llm_connector

    def _generate_system_prompt(self) -> str:
        return ""

    def _generate_user_prompt(self) -> str:
        return ""

    def with_params(self, params: Dict[str, Any]):
        self._params = params
        return self

    def act(self):
        pass

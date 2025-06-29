
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, llm):
        self.llm = llm

    @abstractmethod
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        pass


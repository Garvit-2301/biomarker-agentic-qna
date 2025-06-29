from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.mock_llm_client import MockLLMClient

class BaseAgent(ABC):
    def __init__(self, llm):
        self.llm = llm

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Unified method to generate responses from LLM clients.
        Handles both real LLM clients (with generate method) and MockLLMClient (with generate_response method).
        
        Args:
            prompt: The input prompt
            **kwargs: Additional arguments for the LLM call
            
        Returns:
            Generated text response
        """
        if isinstance(self.llm, MockLLMClient):
            # MockLLMClient uses generate_response and returns a dict
            # Extract agent_type from class name
            agent_type = self._get_agent_type()
            response = self.llm.generate_response(
                prompt=prompt,
                agent_type=agent_type,
                **kwargs
            )
            return response["choices"][0]["message"]["content"]
        else:
            # Real LLM clients use generate and return a string
            return self.llm.generate(prompt, **kwargs)
    
    def _get_agent_type(self) -> str:
        """
        Extract agent type from the class name for MockLLMClient compatibility.
        """
        class_name = self.__class__.__name__.lower()
        
        # Map class names to agent types
        if "insight" in class_name:
            return "analysis"
        elif "qna" in class_name:
            return "analysis"
        elif "explainer" in class_name:
            return "analysis"
        elif "recommendation" in class_name:
            return "recommendation"
        elif "compare" in class_name:
            return "analysis"
        elif "intent" in class_name:
            return "analysis"
        elif "domain" in class_name:
            return "analysis"
        else:
            return "analysis"  # Default fallback

    @abstractmethod
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        pass


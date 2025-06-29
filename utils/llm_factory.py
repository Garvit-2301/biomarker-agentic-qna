from typing import Union
from .openai_client import OpenAIClient
from .llama3_client import Llama3Client

class LLMFactory:
    """
    Factory class to create different LLM clients
    """
    
    @staticmethod
    def create_client(client_type: str = "openai", **kwargs) -> Union[OpenAIClient, Llama3Client]:
        """
        Create an LLM client based on the specified type
        
        Args:
            client_type: Type of client ("openai" or "llama3")
            **kwargs: Additional arguments for the client
            
        Returns:
            LLM client instance
        """
        client_type = client_type.lower()
        
        if client_type == "openai":
            model = kwargs.get("model", "gpt-4")
            return OpenAIClient(model=model)
        
        elif client_type == "llama3":
            return Llama3Client()
        
        else:
            raise ValueError(f"Unsupported client type: {client_type}. Supported types: 'openai', 'llama3'")
    
    @staticmethod
    def get_available_clients() -> list:
        """
        Get list of available client types
        
        Returns:
            List of available client types
        """
        return ["openai", "llama3"]
    
    @staticmethod
    def test_client(client_type: str = "openai", **kwargs) -> bool:
        """
        Test if a client can be created and connected
        
        Args:
            client_type: Type of client to test
            **kwargs: Additional arguments for the client
            
        Returns:
            True if client can be created and connected, False otherwise
        """
        try:
            client = LLMFactory.create_client(client_type, **kwargs)
            return client.test_connection()
        except Exception as e:
            print(f"Error testing {client_type} client: {e}")
            return False 
from openai import OpenAI
import logging
import sys
import os

logging.basicConfig(
    filename='agentic_rag_system.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class OpenAIClient:
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize OpenAI client
        
        Args:
            model: The OpenAI model to use (default: gpt-4)
        """
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        if not api_key:
            logging.error("OPENAI_API_KEY must be provided")
            sys.exit("Environment variable OPENAI_API_KEY is required.")
        
        try:
            self.client = OpenAI(api_key=api_key)
            logging.info(f"Initialized OpenAI client successfully with model {model}.")
        except Exception as exc:
            logging.error("Failed to init OpenAI client: %s", exc)
            sys.exit("Failed to initialize OpenAI client: " + str(exc))

    def generate(self, prompt: str, *, max_tokens: int = 700, temperature: float = 0.7) -> str:
        """
        Generate response using OpenAI API
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate
            temperature: Controls randomness (0.0 = deterministic, 1.0 = very random)
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful microbiome assistant specializing in gut health analysis and personalized recommendations."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logging.error("OpenAI API error: %s", exc)
            return "(OpenAI API error – please try again)"

    def generate_with_context(self, prompt: str, context: str = "", *, max_tokens: int = 700, temperature: float = 0.7) -> str:
        """
        Generate response with additional context
        
        Args:
            prompt: The input prompt
            context: Additional context information
            max_tokens: Maximum tokens to generate
            temperature: Controls randomness
            
        Returns:
            Generated text response
        """
        try:
            messages = [
                {"role": "system", "content": "You are a helpful microbiome assistant specializing in gut health analysis and personalized recommendations."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logging.error("OpenAI API error: %s", exc)
            return "(OpenAI API error – please try again)"

    def get_available_models(self) -> list:
        """
        Get list of available OpenAI models
        
        Returns:
            List of available model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as exc:
            logging.error("Error fetching models: %s", exc)
            return []

    def test_connection(self) -> bool:
        """
        Test the OpenAI API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10,
            )
            return True
        except Exception as exc:
            logging.error("Connection test failed: %s", exc)
 
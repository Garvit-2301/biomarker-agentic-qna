
from openai import OpenAI
import logging, sys, os

logging.basicConfig(
    filename='agentic_rag_system.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class Llama3Client:
    def __init__(self):
        api_key = os.getenv("LLAMA3_API_KEY", "")
        api_url = os.getenv("LLAMA3_API_URL", "")
        if not (api_key and api_url):
            logging.error("LLAMA3_API_KEY / LLAMA3_API_URL must be provided")
            sys.exit("Environment variables LLAMA3_API_KEY and LLAMA3_API_URL are required.")
        try:
            self.client = OpenAI(api_key=api_key, base_url=api_url)
            logging.info("Initialized Llama3Client successfully.")
        except Exception as exc:
            logging.error("Failed to init Llama3 client: %s", exc)
            sys.exit("Failed to initialize Llama3 client: " + str(exc))

    def generate(self, prompt: str, *, max_tokens: int = 700, temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama3.1-70b",
                messages=[
                    {"role": "system", "content": "You are a helpful microbiome assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logging.error("LLM API error: %s", exc)
            return "(LLM error – please try again)"


# Central place for API keys & URLs.
import os

# Llama3 Configuration
LLAMA3_API_KEY = os.getenv("LLAMA3_API_KEY", "")
LLAMA3_API_URL = os.getenv("LLAMA3_API_URL", "")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4")

# System Configuration
DEFAULT_LLM_CLIENT = os.getenv("DEFAULT_LLM_CLIENT", "openai")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


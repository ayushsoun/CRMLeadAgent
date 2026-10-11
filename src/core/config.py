import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    """Enterprise configuration for OpenRouter and application parameters."""
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    # OpenRouter endpoint base URL
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    # Using OpenRouter's automatic free model router
    MODEL_NAME: str = "openrouter/free" 
    TEMPERATURE: float = 0.0

settings = Settings()
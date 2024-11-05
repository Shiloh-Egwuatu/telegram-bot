from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_KEY")

import os

from dotenv import load_dotenv

load_dotenv()

MAX_TOKENS = os.getenv("MAX_TEXT_LEN_TOKENS")
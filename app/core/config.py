import os

from dotenv import load_dotenv


# Load variables from the local .env file
load_dotenv()


APP_NAME = os.getenv(
    "APP_NAME",
    "AI Code Review Assistant",
)

APP_ENV = os.getenv(
    "APP_ENV",
    "development",
)


GITHUB_WEBHOOK_SECRET = os.getenv(
    "GITHUB_WEBHOOK_SECRET",
)

GITHUB_TOKEN = os.getenv(
    "GITHUB_TOKEN",
)

GITHUB_API_URL = "https://api.github.com"

GITHUB_API_VERSION = "2026-03-10"


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna",
)


DRY_RUN = os.getenv(
    "DRY_RUN",
    "true",
).lower() == "true"
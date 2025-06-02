from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN: str

def get_settings():
    return Settings(BOT_TOKEN=os.getenv("BOT_TOKEN"))

import os
from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TILDA_PUBLIC_KEY = os.getenv("TILDA_PUBLIC_KEY")
TILDA_SECRET_KEY = os.getenv("TILDA_SECRET_KEY")

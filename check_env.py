
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print("--- Security Check ---")
if token and len(token) > 10:
    print("✅ TELEGRAM_TOKEN is set correctly.")
else:
    print("❌ TELEGRAM_TOKEN is missing or too short in .env")

if chat_id and len(chat_id) > 5:
    print("✅ TELEGRAM_CHAT_ID is set correctly.")
else:
    print("❌ TELEGRAM_CHAT_ID is missing or too short in .env")

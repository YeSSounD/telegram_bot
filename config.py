import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(id_str.strip()) for id_str in os.getenv('ADMIN_IDS', '').split(',') if id_str.strip()]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не указан в .env файле")
if not ADMIN_IDS:
    print("⚠️ ADMIN_IDS не указаны в .env файле")
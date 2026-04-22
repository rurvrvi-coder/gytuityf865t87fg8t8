import os
import time
import schedule
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATA_FILE = "data.txt"

def get_chat_id():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return f.read().strip()
    return None

def save_chat_id(chat_id):
    with open(DATA_FILE, "w") as f:
        f.write(str(chat_id))

def send_notification():
    chat_id = get_chat_id()
    if not chat_id:
        return
    
    bot = Bot(token=TOKEN)
    now = datetime.now().strftime("%H:%M")
    try:
        bot.send_message(chat_id=int(chat_id), text=f"Уведомление! Время: {now}")
    except TelegramError as e:
        print(f"Ошибка отправки: {e}")

def main():
    if not TOKEN:
        print("Установи TELEGRAM_BOT_TOKEN в .env")
        return
    
    if not get_chat_id():
        print("Отправь боту /start")
    
    print("Бот запущен. Ожидание уведомлений...")
    
    schedule.every(15).minutes.do(send_notification)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
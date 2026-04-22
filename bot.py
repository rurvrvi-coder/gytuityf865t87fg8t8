import os
import threading
import schedule
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATA_FILE = "data.txt"

bot = Bot(token=TOKEN)

def get_chat_id():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return f.read().strip()
    return None

def save_chat_id(chat_id):
    with open(DATA_FILE, "w") as f:
        f.write(str(chat_id))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_chat_id(update.message.chat_id)
    await update.message.reply_text("Готово! Уведомления будут приходить каждые 15 минут.")

def run_scheduler():
    while True:
        schedule.run_pending()
        import time
        time.sleep(60)

def send_notification():
    chat_id = get_chat_id()
    if not chat_id:
        return
    now = datetime.now().strftime("%H:%M")
    try:
        bot.send_message(chat_id=int(chat_id), text=f"Уведомление! Время: {now}")
    except TelegramError as e:
        print(f"Ошибка отправки: {e}")

def main():
    if not TOKEN:
        print("Установи TELEGRAM_BOT_TOKEN в .env")
        return
    
    schedule.every(15).minutes.do(send_notification)
    
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Бот запущен. Отправь /start боту.")
    
    app.run_polling()
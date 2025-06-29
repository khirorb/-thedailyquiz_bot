from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
from flask import Flask

# تحميل المتغيرات من ملف .env
load_dotenv()

# جلب التوكن من متغير البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"🔑 BOT_TOKEN = {BOT_TOKEN}")  # للتأكد من أنه تم تحميل التوكن

# إعداد التطبيق
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# تعريف أمر بسيط للرد بـ "Hello!" عند استخدام /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your bot.")

# إضافة الأمر إلى التطبيق
telegram_app.add_handler(CommandHandler("start", start))

# تشغيل البوت
if __name__ == "__main__":
    telegram_app.run_polling()
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import datetime
import os
from flask import Flask  # نضيف Flask حتى نظهر Web service لـ Render

BOT_TOKEN = os.getenv("8179014874:AAFERf_QggHNnih7Q94TcLo0njetSp6-ous")
print(f"🔑 BOT_TOKEN = {BOT_TOKEN}")  # ← هذا السطر مهم الآن
app = ApplicationBuilder().token(BOT_TOKEN).build()

CHAT_ID_FILE = "chat_id.txt"
CHAT_ID = None

# نحفظ chat_id إذا أرسل /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(CHAT_ID))
    await update.message.reply_text("📌 تم حفظ المجموعة! سأرسل استطلاعًا يوميًا الساعة 9 ليلاً بإذن الله.")

# مهمة إرسال الاستطلاع
async def send_daily_poll(application):
    global CHAT_ID
    # تحميل chat_id من الملف
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            CHAT_ID = int(f.read().strip())
    while True:
        now = datetime.datetime.now()
        if now.hour == 21 and now.minute == 0 and CHAT_ID:
            try:
                await application.bot.send_poll(
                    chat_id=CHAT_ID,
                    question="هل قرأت وردك؟",
                    options=["نعم قرأت وردي الحمد لله", "لا لم أقرأه"],
                    is_anonymous=False
                )
                print("✅ تم إرسال الاستطلاع")
                await asyncio.sleep(60)
            except Exception as e:
                print("❌ خطأ أثناء الإرسال:", e)
        await asyncio.sleep(30)

# Flask app لتوافق Render
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running ✅"

# التشغيل
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    asyncio.create_task(send_daily_poll(app))
    print("🤖 البوت يعمل الآن...")
    app.run_webhook(listen="0.0.0.0", port=10000, webhook_url=None, web_app=web_app)

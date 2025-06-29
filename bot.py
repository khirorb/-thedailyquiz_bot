from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import datetime
import os

BOT_TOKEN = "8179014874:AAFERf_QggHNnih7Q94TcLo0njetSp6-ous"

# تحميل chat_id من الملف إن وُجد
CHAT_ID_FILE = "chat_id.txt"
if os.path.exists(CHAT_ID_FILE):
    with open(CHAT_ID_FILE, "r") as f:
        CHAT_ID = int(f.read().strip())
else:
    CHAT_ID = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(CHAT_ID))
    await update.message.reply_text("تم حفظ المجموعة! سأرسل استطلاعًا يوميًا على الساعة 9 ليلاً إن شاء الله.")

async def send_daily_poll(application):
    global CHAT_ID
    while True:
        now = datetime.datetime.now()
        if now.hour == 21 and now.minute == 0 and CHAT_ID is not None:
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
                print("❌ خطأ أثناء إرسال الاستطلاع:", e)
        await asyncio.sleep(30)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.job_queue.run_once(lambda ctx: asyncio.create_task(send_daily_poll(app)), when=0)
    print("🤖 البوت يعمل الآن...")
    app.run_polling()

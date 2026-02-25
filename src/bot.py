import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== НАСТРОЙКИ =====
TOKEN = os.getenv("BOT_TOKEN")  # можно потом заменить на TOKEN = "ТВОЙ_ТОКЕН"
VIDEO1_ID = "VIDEO1_FILE_ID"
VIDEO2_ID = "VIDEO2_FILE_ID"
BONUS_TEXT = "Вот твоя сказка 🎁"

# ===== ТЕКСТЫ =====
MSG_START = "Привет! Меня зовут Сознание. Готов(а) посмотреть первое видео?"
MSG_WATCH_1 = "Отлично, приятного просмотра 💜"

MSG_AFTER_VIDEO_1 = (
    "Если хочешь, можешь поделиться тем, что запомнилось больше всего.\n\n"
    "Перед следующим видео подготовь блокнот и цветные карандаши."
)

MSG_READY_2 = "Отлично, начинаем. Приятного просмотра 💜"

MSG_AFTER_VIDEO_2 = (
    "Если хочешь, можешь поделиться списком, который получился 💜\n\n"
    "За твоё внимание тебя ждёт бонус 🎁"
)

# ===== КНОПКИ =====
BTN_READY_1 = InlineKeyboardMarkup([
    [InlineKeyboardButton("Да, готов(а)", callback_data="ready_1")]
])

BTN_READY_2 = InlineKeyboardMarkup([
    [InlineKeyboardButton("Готово", callback_data="ready_2")]
])

BTN_BONUS = InlineKeyboardMarkup([
    [InlineKeyboardButton("Получить сказку ✨", callback_data="bonus")]
])

# ===== ХЭНДЛЕРЫ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MSG_START, reply_markup=BTN_READY_1)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ready_1":
        await query.message.reply_text(MSG_WATCH_1)
        await context.bot.send_video(chat_id=query.message.chat_id, video=VIDEO1_ID)
        await query.message.reply_text(MSG_AFTER_VIDEO_1, reply_markup=BTN_READY_2)

    elif query.data == "ready_2":
        await query.message.reply_text(MSG_READY_2)
        await context.bot.send_video(chat_id=query.message.chat_id, video=VIDEO2_ID)
        await query.message.reply_text(MSG_AFTER_VIDEO_2, reply_markup=BTN_BONUS)

    elif query.data == "bonus":
        await query.message.reply_text(BONUS_TEXT)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()

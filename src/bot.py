import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Заглушки для видео — добавишь file_id позже
VIDEO_1_ID = None
VIDEO_2_ID = None
VIDEO_3_ID = None  # сказка (бонус)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Да, готов(а)", callback_data="go_video_1")]
    ]
    text = (
        "Привет!\n"
        "Меня зовут Сознание.\n\n"
        "Готов(а) посмотреть первое видео?"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def on_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "go_video_1":
        await query.message.reply_text("Отлично, приятного просмотра 💜")
        if VIDEO_1_ID:
            await context.bot.send_video(chat_id=query.message.chat_id, video=VIDEO_1_ID)

        keyboard = [
            [InlineKeyboardButton("▶️ Да", callback_data="go_prepare_2")]
        ]
        await query.message.reply_text(
            "Если хочешь, поделись тем, что запомнилось больше всего.\n\n"
            "Хочешь посмотреть следующее видео?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "go_prepare_2":
        keyboard = [
            [InlineKeyboardButton("✏️ Готово", callback_data="go_video_2")]
        ]
        await query.message.reply_text(
            "Для следующего видео понадобятся:\n"
            "– блокнот\n"
            "– цветные карандаши",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "go_video_2":
        await query.message.reply_text("Отлично, начинаем.\nПриятного просмотра 🌟")
        if VIDEO_2_ID:
            await context.bot.send_video(chat_id=query.message.chat_id, video=VIDEO_2_ID)

        keyboard = [
            [InlineKeyboardButton("🎁 Получить сказку", callback_data="get_bonus")]
        ]
        await query.message.reply_text(
            "Если хочешь, поделись списком, который получился.\n\n"
            "За твоё внимание тебя ждёт бонус 🎁",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "get_bonus":
        if VIDEO_3_ID:
            await context.bot.send_video(chat_id=query.message.chat_id, video=VIDEO_3_ID)

def main():
    if not TOKEN:
        raise ValueError("Переменная окружения BOT_TOKEN не найдена")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_buttons))
    app.run_polling()

if __name__ == "__main__":
    main()

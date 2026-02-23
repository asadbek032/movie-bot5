from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from users import add_user, get_users  # 👈 bu modulni import qildik

TOKEN = "7675907648:AAGGiyaM18faJ4ofgydIKkBYOl7OYI5e2U0"
CHANNEL = "@Mov1e5s"

# Menyular
main_menu = ReplyKeyboardMarkup(
    [
        ["🔎 Kino topish"],
        ["🔥 Top kinolar"],
        ["ℹ️ Yordam"]
    ],
    resize_keyboard=True
)

top_movies = {
    "🎬 Qasoskorlar": 4,
    "🎬 Chegarasizlar 2": 9,
    "🎬 Qasoskorlar 4: Intiho": 7
}

top_menu = ReplyKeyboardMarkup(
    [[name] for name in top_movies.keys()] + [["🔙 Orqaga"]],
    resize_keyboard=True
)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)  # 👈 foydalanuvchi qo‘shamiz

    await update.message.reply_text(
        "🎬 Movie 5 botga xush kelibsiz!",
        reply_markup=main_menu
    )

# STATS
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_users()
    total = len(users)
    message = f"👥 Foydalanuvchilar soni: {total}\n\n"
    for uid, info in users.items():
        message += f"{info['first_name']} (@{info['username']})\n"
    await update.message.reply_text(message)

# Xabarlarni ushlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔥 Top kinolar":
        await update.message.reply_text(
            "🔥 Eng mashhur kinolar:",
            reply_markup=top_menu
        )

    elif text == "🔙 Orqaga":
        await update.message.reply_text(
            "Asosiy menyu:",
            reply_markup=main_menu
        )

    elif text == "ℹ️ Yordam":
        await update.message.reply_text(
            "Kino tanlang va bot sizga yuboradi 🎥",
            reply_markup=main_menu
        )

    elif text in top_movies:
        await context.bot.forward_message(
            chat_id=update.effective_chat.id,
            from_chat_id=CHANNEL,
            message_id=top_movies[text]
        )

    else:
        await update.message.reply_text(
            "Iltimos, menyudan tanlang.",
            reply_markup=main_menu
        )

# Application
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")
app.run_polling()
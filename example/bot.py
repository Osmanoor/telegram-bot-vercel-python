from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from os import getenv
import example.generator as generator
import example.memegen as memegen

# Define a few command handlers.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(text="Hi! Send me a description of the meme you want to generate.")
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(text="help me!")
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_description = update.message.text
    await update.message.reply_html(text=f"Generating meme for: {user_description}")

    json_file = "templates.json"
    template_name, texts = generator.generate_meme_from_description(user_description, json_file)
    meme_url = memegen.generate_meme(template_name, texts, 'meme.jpg')

    await update.message.reply_html(text=f"Here is your meme: {meme_url}")

async def bot_tele(text):
    # Create application
    application = (
        Application.builder().token(getenv("TOKEN")).build()
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    # Start application
    # await application.bot.set_webhook(url=getenv("webhook"))
    await application.update_queue.put(
            Update.de_json(data=text, bot=application.bot)
        )
    async with application:
        await application.start()
        await application.stop()
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
TELEGRAM_TOKEN = '7965182442:AAF4vf1eY_mzOQVekKSeqF2ZIyYMNc7nKsE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Sends a greeting message when the bot is started
    await update.message.reply_text('Hello! I am UniBot, here to help you.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Echoes back any message the user sends
    await update.message.reply_text(update.message.text)

def main():
    # Create the Application and pass in the bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).connect_timeout(30).build()

    # Add handlers for the /start command and text messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
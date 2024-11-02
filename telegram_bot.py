import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace this with your actual API token obtained securely
TELEGRAM_API_TOKEN = '7965182442:AAF4vf1eY_mzOQVekKSeqF2ZIyYMNc7nKsE'  # Ensure this is correct

# Set up basic logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command from user %s", update.effective_user.id)
    await update.message.reply_text("Hello! I'm your bot. Send me a message, and I'll echo it back!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info("Echoing message from user %s: %s", update.effective_user.id, user_message)
    await update.message.reply_text(user_message)

# Main function to set up the bot application
async def main():
    # Build the application
    app = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run polling with a managed shutdown
    await app.initialize()
    logger.info("Starting bot polling.")
    await app.start()
    await app.updater.start_polling()

    # Wait indefinitely until the bot is stopped
    try:
        await asyncio.Event().wait()  # Keeps the bot running
    except asyncio.CancelledError:
        # Stop the bot and close resources
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        logger.info("Bot has shut down cleanly.")

# Run the bot in an existing event loop
if __name__ == "__main__":
    asyncio.run(main())
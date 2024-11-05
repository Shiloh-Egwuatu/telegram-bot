import asyncio
from config import TELEGRAM_API_TOKEN
from dotenv import load_dotenv
from logger import logger
from openai_request import get_openai_response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

'''
    Primary functions
'''
# Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create an inline keyboard with a button that says "Get Info"
    keyboard = [
        [InlineKeyboardButton("Get Info", callback_data='info')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! Use the buttons below:", reply_markup=reply_markup)

# Message handler for OpenAI response
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    logger.info(f"Received message: {user_input}")
    bot_response = await asyncio.to_thread(get_openai_response, user_input)  # Call the function from openai_helper
    await update.message.reply_text(bot_response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the /help command is issued."""
    await update.message.reply_text("Need help? I'm here! Type any message, and I'll echo it back to you.")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send an info message when the /info command is issued."""
    await update.message.reply_text("I'm a simple bot created to echo messages and learn new tricks!")


'''
    Special Functions
'''
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button click

    # Check which button was clicked and respond accordingly
    if query.data == 'info':
        await query.edit_message_text("I'm a bot created to demonstrate button handling!")
    elif query.data == 'help':
        await query.edit_message_text("Press /help to learn more about what I can do.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the developer."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')


# Main function to set up the bot application
async def main():
    # Build the application
    app = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))

    app.add_error_handler(error_handler)

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
"""
Agent-Cleo Telegram Bot
Main bot application that handles Telegram interactions
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import config
from agent_handler import AgentHandler

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not config.DEBUG_MODE else logging.DEBUG
)
logger = logging.getLogger(__name__)

# Initialize agent handler
agent_handler = AgentHandler()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    response = agent_handler.handle_command('/start', [])
    await update.message.reply_text(response)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    response = agent_handler.handle_command('/help', [])
    await update.message.reply_text(response)


async def agents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /agents command"""
    response = agent_handler.handle_command('/agents', [])
    await update.message.reply_text(response, parse_mode='Markdown')


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset command"""
    user_id = update.effective_user.id
    if user_id in agent_handler.conversation_history:
        agent_handler.conversation_history[user_id] = []
    response = agent_handler.handle_command('/reset', [])
    await update.message.reply_text(response)


async def task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /task command"""
    args = context.args
    response = agent_handler.handle_command('/task', args)
    await update.message.reply_text(response, parse_mode='Markdown')


async def coach_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /coach command - route to Coach-Cleo"""
    user_id = update.effective_user.id
    args = context.args

    # Show typing indicator
    await update.message.chat.send_action("typing")

    # Process with Coach-Cleo
    message = ' '.join(args) if args else "What should I focus on today?"
    response = agent_handler.process_message(user_id, message, agent_name='Coach-Cleo')

    await update.message.reply_text(response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_id = update.effective_user.id
    message_text = update.message.text

    logger.info(f"User {user_id}: {message_text}")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Process message through agent handler
        response = agent_handler.process_message(user_id, message_text)

        # Send response
        await update.message.reply_text(response)

        logger.info(f"Bot response sent to {user_id}")

    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)
        await update.message.reply_text(
            "I encountered an error processing your message. Please try again or use /help for assistance."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)

    if update and update.effective_message:
        await update.effective_message.reply_text(
            "An error occurred. Please try again or contact support if the issue persists."
        )


def main():
    """Start the bot"""
    # Validate configuration
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure:")
        print("1. You've created a .env file (copy from .env.example)")
        print("2. TELEGRAM_BOT_TOKEN is set (get from @BotFather)")
        print("3. ANTHROPIC_API_KEY is set (from Anthropic Console)")
        print("4. TODOIST_API_TOKEN is set (optional, for task creation)\n")
        return

    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("agents", agents_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("task", task_command))
    application.add_handler(CommandHandler("coach", coach_command))

    # Add message handler for regular text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Agent-Cleo Telegram Bot starting...")
    print("\n" + "="*50)
    print("Agent-Cleo Telegram Bot")
    print("="*50)
    print("Status: Running")
    print(f"Default Agent: {config.DEFAULT_AGENT}")
    print(f"Debug Mode: {config.DEBUG_MODE}")
    print("\nBot is ready to receive messages!")
    print("Press Ctrl+C to stop.\n")
    print("="*50 + "\n")

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

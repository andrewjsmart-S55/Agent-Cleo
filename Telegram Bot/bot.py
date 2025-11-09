"""
Agent-Cleo Telegram Bot
Main bot application that handles Telegram interactions
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
import config
from agent_handler import AgentHandler
from action_manager import ActionManager
from notification_service import NotificationService
from workflow_triggers import WorkflowTriggers
from goal_commands import GoalCommands

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not config.DEBUG_MODE else logging.DEBUG
)
logger = logging.getLogger(__name__)

# Initialize services
action_manager = ActionManager()
notification_service = NotificationService()
agent_handler = AgentHandler(action_manager=action_manager, notification_service=notification_service)
workflow_triggers = WorkflowTriggers(agent_handler=agent_handler, notification_service=notification_service)
goal_commands = GoalCommands()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    response = agent_handler.handle_command('/start', [])
    await update.message.reply_text(response)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    response = """**Agent-Cleo Telegram Bot Help**

**📋 Basic Commands:**
/start - Welcome message and introduction
/help - Show this help message
/agents - List all available agents
/reset - Clear conversation history

**🎯 Goal Management:**
/goals [weekly|short|long|stats|all] - View your goals
/focus - Get your #1 priority for today
/weekly_planning - Start weekly goal planning with Coach-Cleo
/goal_review [daily|weekly|monthly] - Review goal progress
/briefing - Get your daily briefing

**🔔 Actions & Approvals:**
/pending - View actions awaiting your approval
/history - View recent action history
/task [description] - Create a task in Todoist

**🤖 Agent Workflows:**
/coach [message] - Talk to Coach-Cleo
/agent_run <agent> <workflow> - Trigger agent workflow
  Examples:
  • /agent_run Coach-Cleo plan
  • /agent_run DecideWright-MD analyze

**💬 Natural Conversation:**
Just message me naturally and I'll route to the right agent!

**Examples:**
• "What should I focus on today?" → Coach-Cleo
• "Create a task to review QRA playbook" → Task creation
• "Show my weekly goals" → Goal view
• "How's my DecideWright project going?" → DecideWright-MD"""

    await update.message.reply_text(response, parse_mode='Markdown')


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


async def pending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pending command - show pending approvals"""
    user_id = update.effective_user.id
    pending_actions = action_manager.get_pending_actions(user_id)

    if not pending_actions:
        await update.message.reply_text("No pending actions requiring approval.")
        return

    for action in pending_actions:
        # Format action for display
        message_text = action_manager.format_action_for_display(action)

        # Create inline keyboard for approval
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{action['id']}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{action['id']}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /history command - show action history"""
    user_id = update.effective_user.id
    history = action_manager.get_history(user_id, limit=10)

    if not history:
        await update.message.reply_text("No action history yet.")
        return

    response = "**Recent Actions**\n\n"
    for action in history:
        status_icon = "✅" if action['status'] == 'approved' else "❌"
        response += f"{status_icon} {action['description'][:50]}...\n"
        response += f"   Agent: {action['agent_name']} | {action['updated_at'][:10]}\n\n"

    await update.message.reply_text(response, parse_mode='Markdown')


async def goals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /goals command - show goals"""
    args = context.args

    if not args or args[0] == "all":
        response = goal_commands.show_all_goals()
    elif args[0] == "weekly":
        response = goal_commands.show_weekly_goals()
    elif args[0] == "short":
        response = goal_commands.show_short_term_goals()
    elif args[0] == "long":
        response = goal_commands.show_long_term_goals()
    elif args[0] == "stats":
        response = goal_commands.get_goal_stats()
    else:
        response = goal_commands.show_all_goals()

    await update.message.reply_text(response, parse_mode='Markdown')


async def focus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /focus command - get focus recommendation"""
    response = goal_commands.get_focus_recommendation()
    await update.message.reply_text(response, parse_mode='Markdown')


async def weekly_planning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weekly_planning command - trigger weekly planning"""
    user_id = update.effective_user.id
    await update.message.reply_text("Starting your weekly planning session with Coach-Cleo...")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    response = workflow_triggers.trigger_weekly_planning(user_id)
    await update.message.reply_text(response, parse_mode='Markdown')


async def goal_review_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /goal_review command"""
    user_id = update.effective_user.id
    args = context.args
    review_type = args[0] if args else "daily"

    await update.message.reply_text(f"Running {review_type} goal review...")
    await update.message.chat.send_action("typing")

    response = workflow_triggers.trigger_goal_review(user_id, review_type)
    await update.message.reply_text(response, parse_mode='Markdown')


async def briefing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /briefing command - daily briefing"""
    user_id = update.effective_user.id
    response = workflow_triggers.trigger_daily_briefing(user_id)
    await update.message.reply_text(response, parse_mode='Markdown')


async def agent_run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /agent_run command - trigger agent workflow"""
    user_id = update.effective_user.id
    args = context.args

    if len(args) < 2:
        await update.message.reply_text(
            "Usage: /agent_run <agent-name> <workflow-type>\n\n"
            "Example: /agent_run DecideWright-MD analyze"
        )
        return

    agent_name = args[0]
    workflow_type = args[1]
    context_text = ' '.join(args[2:]) if len(args) > 2 else None

    await update.message.reply_text(f"Triggering {workflow_type} workflow for {agent_name}...")
    await update.message.chat.send_action("typing")

    response = workflow_triggers.trigger_agent_workflow(
        user_id=user_id,
        agent_name=agent_name,
        workflow_type=workflow_type,
        context={"additional_context": context_text} if context_text else None
    )

    await update.message.reply_text(response)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    callback_data = query.data

    if callback_data.startswith("approve_"):
        action_id = callback_data.replace("approve_", "")

        try:
            action = action_manager.approve_action(action_id, approved_by=user_id)

            # Execute the approved action
            if action['action_type'] == 'create_task':
                # Execute task creation
                from todoist_integration import create_task_for_andrew
                task_data = action['action_data']
                result = create_task_for_andrew(
                    content=task_data.get('task_details'),
                    project=task_data.get('project', 'Personal'),
                    priority=task_data.get('priority', 2),
                    due=task_data.get('due'),
                    agent=action['agent_name']
                )

                if result.get('success'):
                    await query.edit_message_text(
                        f"✅ **Approved and Executed**\n\n{action['description']}\n\nTask created in Todoist!",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text(
                        f"✅ Approved but execution failed: {result.get('error')}",
                        parse_mode='Markdown'
                    )
            else:
                await query.edit_message_text(
                    f"✅ **Approved**\n\n{action['description']}\n\nAction type '{action['action_type']}' approved.",
                    parse_mode='Markdown'
                )

        except Exception as e:
            logger.error(f"Error approving action: {e}")
            await query.edit_message_text(f"Error approving action: {str(e)}")

    elif callback_data.startswith("reject_"):
        action_id = callback_data.replace("reject_", "")

        try:
            action = action_manager.reject_action(action_id, rejected_by=user_id, reason="User rejected")
            await query.edit_message_text(
                f"❌ **Rejected**\n\n{action['description']}",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error rejecting action: {e}")
            await query.edit_message_text(f"Error rejecting action: {str(e)}")


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

    # New command handlers
    application.add_handler(CommandHandler("pending", pending_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("goals", goals_command))
    application.add_handler(CommandHandler("focus", focus_command))
    application.add_handler(CommandHandler("weekly_planning", weekly_planning_command))
    application.add_handler(CommandHandler("goal_review", goal_review_command))
    application.add_handler(CommandHandler("briefing", briefing_command))
    application.add_handler(CommandHandler("agent_run", agent_run_command))

    # Add callback handler for inline keyboards
    application.add_handler(CallbackQueryHandler(callback_handler))

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

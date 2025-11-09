# Quick Setup Instructions

Your Telegram bot is almost ready! You just need to add your API keys.

## Step 1: Get Your Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send: `/newbot`
3. Follow prompts to create your bot
4. Copy the token (looks like: `1234567890:ABCdefGHIjklMNOpqrSTUvwxyz`)

## Step 2: Get Your Anthropic API Key

1. Go to: https://console.anthropic.com/settings/keys
2. Create a new API key
3. Copy the key (starts with `sk-ant-`)

## Step 3: Get Your Todoist API Token (Optional)

1. Go to: https://todoist.com/app/settings/integrations/developer
2. Scroll to "API token"
3. Copy your token

## Step 4: Update the `.env` File

Edit `/home/user/Agent-Cleo/Telegram Bot/.env` and replace the placeholder values:

```bash
TELEGRAM_BOT_TOKEN=paste_your_telegram_token_here
ANTHROPIC_API_KEY=paste_your_anthropic_key_here
TODOIST_API_TOKEN=paste_your_todoist_token_here
```

## Step 5: Run the Bot

```bash
cd "/home/user/Agent-Cleo/Telegram Bot"
python bot.py
```

You should see:
```
==================================================
Agent-Cleo Telegram Bot
==================================================
Status: Running
```

## Step 6: Test in Telegram

1. Find your bot in Telegram (search for the username you created)
2. Send: `/start`
3. Try: `/help` to see all commands
4. Ask: "What should I focus on today?"

---

## Troubleshooting

**Bot doesn't respond:**
- Check that bot.py is running (see "Status: Running")
- Verify all tokens in .env are correct
- Make sure you're messaging the right bot username

**"Configuration Error" on startup:**
- Check .env file exists
- Verify no extra spaces around tokens
- Make sure tokens don't have quotes

**Need help?**
Check the full documentation: `TELEGRAM_BOT_GUIDE.md`

# Agent-Cleo Telegram Bot - Quick Start

**Get your bot running in 10 minutes!**

---

## ⚡ 3-Step Setup

### 1️⃣ Create Bot (5 min)

1. Open Telegram → Search `@BotFather`
2. Type `/newbot`
3. Name it: `Agent-Cleo` (or whatever you like)
4. Username: `your_name_agent_cleo_bot` (must end with 'bot')
5. **SAVE THE TOKEN!** Looks like: `1234567890:ABCdefGHI...`

---

### 2️⃣ Configure (3 min)

1. **Copy environment template:**
   ```bash
   cd "C:\Users\AndrewSmart\Claude_Projects\Agent-Cleo\Telegram Bot"
   copy .env.example .env
   ```

2. **Edit `.env` file** with your tokens:
   - `TELEGRAM_BOT_TOKEN` = Token from BotFather
   - `ANTHROPIC_API_KEY` = Get from https://console.anthropic.com/settings/keys
   - `TODOIST_API_TOKEN` = Already set in main project (optional)

3. **Install packages:**
   ```bash
   pip install -r requirements.txt
   ```

---

### 3️⃣ Run (1 min)

```bash
python bot.py
```

**You should see:**
```
🤖 Agent-Cleo Telegram Bot
Status: Running
Bot is ready to receive messages!
```

✅ **Done! Go to Telegram and message your bot!**

---

## 🎮 Try These First Messages

**1. Start the conversation:**
```
/start
```

**2. Get help:**
```
/help
```

**3. Talk to Coach-Cleo:**
```
What should I focus on today?
```

**4. Create a task:**
```
/task Email client by Friday
```

**5. See all agents:**
```
/agents
```

---

## 🆘 Something Wrong?

### Bot doesn't respond?
- Is `python bot.py` running? Check terminal
- Did you message the correct bot username?
- Restart: `Ctrl+C` then `python bot.py` again

### "Configuration Error"?
- Check `.env` file exists
- Verify tokens are correct (no quotes, no spaces)
- Make sure TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY are set

### Need more help?
See full `README.md` for detailed troubleshooting

---

**That's it! You're ready to coach on-the-go with Agent-Cleo.** 💪

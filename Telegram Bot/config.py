"""
Configuration for Agent-Cleo Telegram Bot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

# Agent-Cleo Paths
PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR = PROJECT_ROOT
PERSONAL_AGENTS_DIR = AGENTS_DIR / "Personal Agents"
TEAM_AGENTS_DIR = AGENTS_DIR / "Team Agents"
WORKER_AGENTS_DIR = AGENTS_DIR / "Worker Agents"
EXPERT_AGENTS_DIR = AGENTS_DIR / "Expert Agents"

# Default Settings
DEFAULT_AGENT = os.getenv('DEFAULT_AGENT', 'Coach-Cleo')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# Claude Configuration
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096

# Agent Routing Keywords
AGENT_KEYWORDS = {
    'coach': 'Coach-Cleo',
    'coaching': 'Coach-Cleo',
    'goal': 'Coach-Cleo',
    'health': 'HealthFit-Agent',
    'fitness': 'HealthFit-Agent',
    'workout': 'HealthFit-Agent',
    'decidewright': 'DecideWright-MD',
    'qra': 'DecideWright-MD',
    'studio55': 'S55-MD',
    'studio': 'S55-MD',
    'apportal': 'S55-MD',
    'thintanks': 'ThinTanks-MD',
    'marketing': 'Agent-CMO',
    'sales': 'Agent-CSO',
    'finance': 'Agent-FD',
    'legal': 'Agent-Legal',
}

def validate_config():
    """Validate that all required configuration is present"""
    errors = []

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is not set")
    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is not set")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

    return True

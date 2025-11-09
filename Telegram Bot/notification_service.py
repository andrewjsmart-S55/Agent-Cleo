"""
Notification Service for Agent-Cleo Telegram Bot
Handles proactive notifications and agent updates
"""
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Manages notifications and proactive agent updates"""

    def __init__(self, data_dir: Path = None, agents_dir: Path = None):
        """
        Initialize NotificationService

        Args:
            data_dir: Directory to store notification data
            agents_dir: Root directory of Agent-Cleo agents
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"

        if agents_dir is None:
            agents_dir = Path(__file__).parent.parent

        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)

        self.agents_dir = agents_dir
        self.notifications_file = self.data_dir / "notifications.json"
        self.watchers_file = self.data_dir / "output_watchers.json"

        # Load existing data
        self.notifications = self._load_notifications()
        self.output_watchers = self._load_watchers()

    def _load_notifications(self) -> List:
        """Load notification queue from file"""
        if self.notifications_file.exists():
            try:
                with open(self.notifications_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading notifications: {e}")
        return []

    def _load_watchers(self) -> Dict:
        """Load output watchers from file"""
        if self.watchers_file.exists():
            try:
                with open(self.watchers_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading watchers: {e}")
        return {}

    def _save_notifications(self):
        """Save notifications to file"""
        try:
            with open(self.notifications_file, 'w') as f:
                json.dump(self.notifications, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving notifications: {e}")

    def _save_watchers(self):
        """Save watchers to file"""
        try:
            with open(self.watchers_file, 'w') as f:
                json.dump(self.output_watchers, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving watchers: {e}")

    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "info",
        agent_name: str = None,
        scheduled_for: datetime = None,
        priority: int = 2
    ) -> str:
        """
        Create a notification

        Args:
            user_id: Telegram user ID
            title: Notification title
            message: Notification message
            notification_type: Type (info, warning, success, action_required)
            agent_name: Agent that created notification
            scheduled_for: When to send (None = immediate)
            priority: Priority level (1=high, 2=normal, 3=low)

        Returns:
            Notification ID
        """
        notification_id = f"notif_{int(time.time() * 1000)}"

        notification = {
            "id": notification_id,
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "agent_name": agent_name,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "scheduled_for": scheduled_for.isoformat() if scheduled_for else None,
            "sent_at": None
        }

        self.notifications.append(notification)
        self._save_notifications()

        logger.info(f"Created notification {notification_id} for user {user_id}")
        return notification_id

    def get_pending_notifications(self, user_id: int = None) -> List[Dict]:
        """
        Get pending notifications ready to be sent

        Args:
            user_id: Filter by user ID (optional)

        Returns:
            List of pending notifications
        """
        now = datetime.now()
        pending = []

        for notif in self.notifications:
            if notif['status'] != 'pending':
                continue

            if user_id and notif['user_id'] != user_id:
                continue

            # Check if scheduled notification is ready
            if notif['scheduled_for']:
                scheduled_time = datetime.fromisoformat(notif['scheduled_for'])
                if scheduled_time > now:
                    continue

            pending.append(notif)

        return pending

    def mark_sent(self, notification_id: str):
        """Mark a notification as sent"""
        for notif in self.notifications:
            if notif['id'] == notification_id:
                notif['status'] = 'sent'
                notif['sent_at'] = datetime.now().isoformat()
                self._save_notifications()
                logger.info(f"Marked notification {notification_id} as sent")
                return

    def watch_agent_output(self, agent_name: str, user_id: int):
        """
        Start watching an agent's Output folder for new files

        Args:
            agent_name: Name of agent to watch
            user_id: User to notify
        """
        # Find agent directory
        agent_dirs = [
            self.agents_dir / "Personal Agents" / agent_name,
            self.agents_dir / "Team Agents" / agent_name,
            self.agents_dir / "Worker Agents" / agent_name,
            self.agents_dir / "Expert Agents" / agent_name,
        ]

        output_dir = None
        for agent_dir in agent_dirs:
            if agent_dir.exists():
                output_dir = agent_dir / "Output"
                break

        if not output_dir or not output_dir.exists():
            logger.warning(f"Output directory not found for agent {agent_name}")
            return

        # Get current files and their modification times
        current_files = {}
        for file_path in output_dir.glob("*"):
            if file_path.is_file():
                current_files[str(file_path)] = file_path.stat().st_mtime

        # Store watcher
        watcher_id = f"{agent_name}_{user_id}"
        self.output_watchers[watcher_id] = {
            "agent_name": agent_name,
            "user_id": user_id,
            "output_dir": str(output_dir),
            "last_check": datetime.now().isoformat(),
            "known_files": current_files
        }

        self._save_watchers()
        logger.info(f"Started watching {agent_name} output for user {user_id}")

    def check_output_changes(self) -> List[Dict]:
        """
        Check all watched output folders for changes

        Returns:
            List of change notifications
        """
        changes = []

        for watcher_id, watcher in self.output_watchers.items():
            output_dir = Path(watcher['output_dir'])

            if not output_dir.exists():
                continue

            # Check for new or modified files
            current_files = {}
            for file_path in output_dir.glob("*"):
                if file_path.is_file():
                    mtime = file_path.stat().st_mtime
                    current_files[str(file_path)] = mtime

                    # Check if new or modified
                    known_mtime = watcher['known_files'].get(str(file_path))

                    if known_mtime is None:
                        # New file
                        changes.append({
                            "watcher_id": watcher_id,
                            "user_id": watcher['user_id'],
                            "agent_name": watcher['agent_name'],
                            "change_type": "new_file",
                            "file_path": str(file_path),
                            "file_name": file_path.name
                        })
                    elif mtime > known_mtime:
                        # Modified file
                        changes.append({
                            "watcher_id": watcher_id,
                            "user_id": watcher['user_id'],
                            "agent_name": watcher['agent_name'],
                            "change_type": "modified_file",
                            "file_path": str(file_path),
                            "file_name": file_path.name
                        })

            # Update watcher
            watcher['known_files'] = current_files
            watcher['last_check'] = datetime.now().isoformat()

        if changes:
            self._save_watchers()

        return changes

    def format_notification(self, notification: Dict) -> str:
        """Format a notification for display"""
        # Icon based on type
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "success": "✅",
            "action_required": "🔔"
        }

        icon = icons.get(notification['type'], "📬")
        agent = f" - {notification['agent_name']}" if notification.get('agent_name') else ""

        lines = [
            f"{icon} **{notification['title']}**{agent}",
            "",
            notification['message']
        ]

        return '\n'.join(lines)

    def create_daily_briefing(self, user_id: int) -> str:
        """
        Create a daily briefing notification

        Args:
            user_id: User ID

        Returns:
            Notification ID
        """
        # This would integrate with goal_helper and todoist_integration
        # to create a comprehensive daily briefing

        from datetime import datetime

        today = datetime.now().strftime("%A, %B %d")

        message = f"""Good morning! Here's your briefing for {today}.

**Your Focus Today:**
Review your weekly goals and identify your #1 priority.

**Quick Actions:**
• /goals weekly - View your weekly goals
• /coach What should I focus on today?
• /pending - Check any pending approvals

Have a productive day!"""

        return self.create_notification(
            user_id=user_id,
            title="Daily Briefing",
            message=message,
            notification_type="info",
            agent_name="Coach-Cleo",
            priority=2
        )

    def schedule_reminder(
        self,
        user_id: int,
        reminder_text: str,
        scheduled_for: datetime,
        agent_name: str = None
    ) -> str:
        """
        Schedule a reminder notification

        Args:
            user_id: User ID
            reminder_text: Reminder message
            scheduled_for: When to send reminder
            agent_name: Agent creating the reminder

        Returns:
            Notification ID
        """
        return self.create_notification(
            user_id=user_id,
            title="Reminder",
            message=reminder_text,
            notification_type="info",
            agent_name=agent_name,
            scheduled_for=scheduled_for,
            priority=2
        )

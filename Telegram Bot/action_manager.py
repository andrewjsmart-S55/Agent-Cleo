"""
Action Manager for Agent-Cleo Telegram Bot
Handles action approval workflow and queuing
"""
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ActionManager:
    """Manages pending actions that require user approval"""

    def __init__(self, data_dir: Path = None):
        """
        Initialize ActionManager

        Args:
            data_dir: Directory to store action data (default: Telegram Bot/data)
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"

        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)

        self.pending_file = self.data_dir / "pending_actions.json"
        self.history_file = self.data_dir / "action_history.json"

        # Load existing data
        self.pending_actions = self._load_pending()
        self.action_history = self._load_history()

    def _load_pending(self) -> Dict:
        """Load pending actions from file"""
        if self.pending_file.exists():
            try:
                with open(self.pending_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading pending actions: {e}")
        return {}

    def _load_history(self) -> List:
        """Load action history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading action history: {e}")
        return []

    def _save_pending(self):
        """Save pending actions to file"""
        try:
            with open(self.pending_file, 'w') as f:
                json.dump(self.pending_actions, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving pending actions: {e}")

    def _save_history(self):
        """Save action history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.action_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving action history: {e}")

    def create_action(
        self,
        user_id: int,
        agent_name: str,
        action_type: str,
        description: str,
        action_data: Dict,
        context: str = ""
    ) -> str:
        """
        Create a new action requiring approval

        Args:
            user_id: Telegram user ID
            agent_name: Name of the agent requesting action
            action_type: Type of action (create_task, send_email, etc.)
            description: Human-readable description
            action_data: Data needed to execute the action
            context: Additional context for the user

        Returns:
            Action ID
        """
        action_id = f"{int(time.time() * 1000)}"

        action = {
            "id": action_id,
            "user_id": user_id,
            "agent_name": agent_name,
            "action_type": action_type,
            "description": description,
            "action_data": action_data,
            "context": context,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        self.pending_actions[action_id] = action
        self._save_pending()

        logger.info(f"Created action {action_id} for user {user_id}")
        return action_id

    def get_pending_actions(self, user_id: int) -> List[Dict]:
        """Get all pending actions for a user"""
        return [
            action for action in self.pending_actions.values()
            if action['user_id'] == user_id and action['status'] == 'pending'
        ]

    def get_action(self, action_id: str) -> Optional[Dict]:
        """Get a specific action by ID"""
        return self.pending_actions.get(action_id)

    def approve_action(self, action_id: str, approved_by: int = None) -> Dict:
        """
        Approve an action

        Args:
            action_id: Action ID to approve
            approved_by: User ID who approved (optional)

        Returns:
            Updated action dict
        """
        if action_id not in self.pending_actions:
            raise ValueError(f"Action {action_id} not found")

        action = self.pending_actions[action_id]
        action['status'] = 'approved'
        action['approved_by'] = approved_by
        action['approved_at'] = datetime.now().isoformat()
        action['updated_at'] = datetime.now().isoformat()

        # Move to history
        self.action_history.append(action)
        del self.pending_actions[action_id]

        self._save_pending()
        self._save_history()

        logger.info(f"Action {action_id} approved")
        return action

    def reject_action(self, action_id: str, rejected_by: int = None, reason: str = "") -> Dict:
        """
        Reject an action

        Args:
            action_id: Action ID to reject
            rejected_by: User ID who rejected (optional)
            reason: Reason for rejection

        Returns:
            Updated action dict
        """
        if action_id not in self.pending_actions:
            raise ValueError(f"Action {action_id} not found")

        action = self.pending_actions[action_id]
        action['status'] = 'rejected'
        action['rejected_by'] = rejected_by
        action['rejected_at'] = datetime.now().isoformat()
        action['rejection_reason'] = reason
        action['updated_at'] = datetime.now().isoformat()

        # Move to history
        self.action_history.append(action)
        del self.pending_actions[action_id]

        self._save_pending()
        self._save_history()

        logger.info(f"Action {action_id} rejected: {reason}")
        return action

    def modify_action(self, action_id: str, new_data: Dict) -> Dict:
        """
        Modify an action's data before approval

        Args:
            action_id: Action ID to modify
            new_data: Updated action data

        Returns:
            Updated action dict
        """
        if action_id not in self.pending_actions:
            raise ValueError(f"Action {action_id} not found")

        action = self.pending_actions[action_id]
        action['action_data'].update(new_data)
        action['updated_at'] = datetime.now().isoformat()

        self._save_pending()

        logger.info(f"Action {action_id} modified")
        return action

    def get_history(self, user_id: int, limit: int = 20) -> List[Dict]:
        """
        Get action history for a user

        Args:
            user_id: User ID
            limit: Maximum number of actions to return

        Returns:
            List of historical actions (most recent first)
        """
        user_history = [
            action for action in self.action_history
            if action['user_id'] == user_id
        ]

        # Sort by updated_at, most recent first
        user_history.sort(key=lambda x: x['updated_at'], reverse=True)

        return user_history[:limit]

    def get_stats(self, user_id: int) -> Dict:
        """Get statistics about user's actions"""
        history = [a for a in self.action_history if a['user_id'] == user_id]
        pending = self.get_pending_actions(user_id)

        approved = [a for a in history if a['status'] == 'approved']
        rejected = [a for a in history if a['status'] == 'rejected']

        return {
            'pending': len(pending),
            'total_history': len(history),
            'approved': len(approved),
            'rejected': len(rejected),
            'approval_rate': (len(approved) / len(history) * 100) if history else 0
        }

    def format_action_for_display(self, action: Dict) -> str:
        """Format an action for display in Telegram"""
        lines = [
            f"**Action #{action['id'][-6:]}**",
            f"Agent: {action['agent_name']}",
            f"Type: {action['action_type']}",
            f"",
            f"**Description:**",
            f"{action['description']}",
        ]

        if action.get('context'):
            lines.extend([
                f"",
                f"**Context:**",
                f"{action['context']}"
            ])

        # Format action data based on type
        if action['action_type'] == 'create_task':
            data = action['action_data']
            lines.extend([
                f"",
                f"**Task Details:**",
                f"• Task: {data.get('task_details', 'N/A')}",
                f"• Project: {data.get('project', 'Personal')}",
                f"• Priority: P{data.get('priority', 2)}",
                f"• Due: {data.get('due', 'Not set')}"
            ])

        lines.append(f"\nCreated: {action['created_at'][:16]}")

        return '\n'.join(lines)

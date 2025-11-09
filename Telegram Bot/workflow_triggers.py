"""
Workflow Triggers for Agent-Cleo Telegram Bot
Handles triggered agent workflows and automation
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class WorkflowTriggers:
    """Manages agent workflow triggers and automation"""

    def __init__(self, agent_handler, notification_service):
        """
        Initialize WorkflowTriggers

        Args:
            agent_handler: AgentHandler instance for agent communication
            notification_service: NotificationService for sending updates
        """
        self.agent_handler = agent_handler
        self.notification_service = notification_service

        # Add goal_helper to path
        self.project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(self.project_root))
        sys.path.insert(0, str(self.project_root / "Personal Agents" / "Coach-Cleo" / "Context"))

    def trigger_weekly_planning(self, user_id: int) -> str:
        """
        Trigger Coach-Cleo's weekly planning session

        Args:
            user_id: User ID

        Returns:
            Planning session output
        """
        try:
            from goal_helper import (
                get_weekly_goals,
                get_short_term_goals,
                get_active_weekly_goals,
                get_completed_weekly_goals,
                calculate_weekly_completion_rate
            )

            # Get current goals
            weekly_goals = get_weekly_goals()
            short_term_goals = get_short_term_goals()
            active_weekly = get_active_weekly_goals()
            completed_weekly = get_completed_weekly_goals()
            completion_rate = calculate_weekly_completion_rate()

            # Build context for Coach-Cleo
            context = f"""
**Weekly Planning Session - {datetime.now().strftime('%B %d, %Y')}**

**Last Week's Performance:**
- Weekly Goals Set: {len(weekly_goals)}
- Completed: {len(completed_weekly)} ({completion_rate}%)
- Still Active: {len(active_weekly)}

**Completed Goals:**
"""
            for goal in completed_weekly[:5]:  # Show last 5 completed
                context += f"✅ {goal['content']}\n"

            if active_weekly:
                context += f"\n**Incomplete Goals:**\n"
                for goal in active_weekly:
                    context += f"⏸️ {goal['content']}\n"

            context += f"\n**Short Term Goals (Context):**\n"
            for goal in short_term_goals[:5]:  # Show top 5
                context += f"• {goal['content']}\n"

            # Trigger Coach-Cleo with planning prompt
            planning_prompt = f"""{context}

Please help me plan this week following the Goal Management Framework:

1. Review last week's performance
2. Analyze what worked and what didn't
3. Recommend 3-5 Weekly Goals for this week
4. Ensure each goal:
   - Supports a Short Term Goal
   - Is achievable this week
   - Has clear "done" criteria
   - Is due Friday

Let's create a focused, achievable plan for this week."""

            response = self.agent_handler.process_message(
                user_id=user_id,
                message=planning_prompt,
                agent_name='Coach-Cleo'
            )

            # Create notification about planning session
            self.notification_service.create_notification(
                user_id=user_id,
                title="Weekly Planning Complete",
                message="Your weekly planning session is ready. Review your goals and commit to the week ahead!",
                notification_type="success",
                agent_name="Coach-Cleo",
                priority=1
            )

            return response

        except Exception as e:
            logger.error(f"Error in weekly planning: {e}", exc_info=True)
            return f"Error during weekly planning: {str(e)}\n\nPlease ensure goal_helper.py is properly configured."

    def trigger_goal_review(self, user_id: int, review_type: str = "daily") -> str:
        """
        Trigger a goal review session

        Args:
            user_id: User ID
            review_type: Type of review (daily, weekly, monthly, quarterly)

        Returns:
            Review output
        """
        try:
            from goal_helper import (
                get_active_weekly_goals,
                get_short_term_goals,
                get_long_term_goals,
                calculate_weekly_completion_rate
            )

            active_weekly = get_active_weekly_goals()
            completion_rate = calculate_weekly_completion_rate()

            if review_type == "daily":
                # Quick daily check-in
                prompt = f"""Quick daily goal check-in:

**Active Weekly Goals ({len(active_weekly)}):**
"""
                for i, goal in enumerate(active_weekly, 1):
                    due_date = goal.get('due', {})
                    due_str = due_date.get('date', 'No due date') if isinstance(due_date, dict) else due_date
                    prompt += f"{i}. {goal['content']} (Due: {due_str})\n"

                prompt += f"\nWeekly Completion Rate: {completion_rate}%\n\n"
                prompt += "Questions for today:\n"
                prompt += "1. Which Weekly Goal will I focus on today?\n"
                prompt += "2. Any blockers I need to address?\n"
                prompt += "3. What's my one priority for today?"

            elif review_type == "weekly":
                # Weekly review
                prompt = f"""Weekly goal review:

**This Week's Progress:**
- Completion Rate: {completion_rate}%
- Active Goals: {len(active_weekly)}

**Active Goals:**
"""
                for goal in active_weekly:
                    prompt += f"• {goal['content']}\n"

                prompt += "\nReflection:\n"
                prompt += "1. What progress was made this week?\n"
                prompt += "2. What's blocking completion?\n"
                prompt += "3. Do I need to adjust any goals?\n"
                prompt += "4. What's the plan for finishing strong?"

            elif review_type == "monthly":
                short_term = get_short_term_goals()
                prompt = f"""Monthly goal review:

**Weekly Performance:**
- Average Completion Rate: {completion_rate}%

**Short Term Goals ({len(short_term)}):**
"""
                for goal in short_term:
                    prompt += f"• {goal['content']}\n"

                prompt += "\nMonthly Review Questions:\n"
                prompt += "1. Which Short Term Goals made progress?\n"
                prompt += "2. Which are being neglected?\n"
                prompt += "3. Are we on track for our targets?\n"
                prompt += "4. What needs to change next month?"

            else:  # quarterly
                long_term = get_long_term_goals()
                short_term = get_short_term_goals()

                prompt = f"""Quarterly strategic review:

**Long Term Goals ({len(long_term)}):**
"""
                for goal in long_term:
                    prompt += f"• {goal['content']}\n"

                prompt += f"\n**Short Term Goals ({len(short_term)}):**\n"
                for goal in short_term:
                    prompt += f"• {goal['content']}\n"

                prompt += "\nQuarterly Review:\n"
                prompt += "1. Progress toward Long Term Goals?\n"
                prompt += "2. Completion rate and patterns?\n"
                prompt += "3. What worked, what didn't?\n"
                prompt += "4. OKRs for next quarter?"

            # Get Coach-Cleo's review
            response = self.agent_handler.process_message(
                user_id=user_id,
                message=prompt,
                agent_name='Coach-Cleo'
            )

            return response

        except Exception as e:
            logger.error(f"Error in goal review: {e}", exc_info=True)
            return f"Error during goal review: {str(e)}"

    def trigger_daily_briefing(self, user_id: int) -> str:
        """
        Trigger morning daily briefing

        Args:
            user_id: User ID

        Returns:
            Briefing output
        """
        try:
            from goal_helper import get_active_weekly_goals
            from todoist_integration import get_tasks_by_label

            active_goals = get_active_weekly_goals()

            # Get today's tasks
            today_tasks = []
            try:
                all_tasks = get_tasks_by_label("Agent-Cleo")
                today = datetime.now().date()
                for task in all_tasks:
                    if task.get('due'):
                        due_date = task['due'].get('date') if isinstance(task['due'], dict) else task['due']
                        if due_date and str(today) in str(due_date):
                            today_tasks.append(task)
            except:
                pass

            briefing = f"""**Daily Briefing - {datetime.now().strftime('%A, %B %d')}**

**Your Weekly Goals ({len(active_goals)} active):**
"""
            for i, goal in enumerate(active_goals[:3], 1):  # Top 3
                briefing += f"{i}. {goal['content']}\n"

            if today_tasks:
                briefing += f"\n**Today's Tasks ({len(today_tasks)}):**\n"
                for task in today_tasks[:5]:
                    briefing += f"• {task.get('content', 'Task')}\n"

            briefing += "\n**Quick Questions:**\n"
            briefing += "• What's your #1 priority today?\n"
            briefing += "• Which goal will you make progress on?\n"
            briefing += "• Any blockers to address?"

            return briefing

        except Exception as e:
            logger.error(f"Error creating briefing: {e}", exc_info=True)
            return f"Error creating daily briefing: {str(e)}"

    def trigger_focus_check(self, user_id: int) -> str:
        """
        Quick focus check - what's the ONE thing today?

        Args:
            user_id: User ID

        Returns:
            Focus recommendation
        """
        try:
            from goal_helper import get_active_weekly_goals

            active_goals = get_active_weekly_goals()

            if not active_goals:
                return "You don't have any active Weekly Goals. Consider running /weekly_planning to set your goals for the week."

            prompt = f"""Focus Check:

You have {len(active_goals)} active Weekly Goals:

"""
            for i, goal in enumerate(active_goals, 1):
                prompt += f"{i}. {goal['content']}\n"

            prompt += "\nWhich ONE goal should be your priority today? What single action would create the most progress?"

            response = self.agent_handler.process_message(
                user_id=user_id,
                message=prompt,
                agent_name='Coach-Cleo'
            )

            return response

        except Exception as e:
            logger.error(f"Error in focus check: {e}", exc_info=True)
            return f"Error during focus check: {str(e)}"

    def trigger_agent_workflow(
        self,
        user_id: int,
        agent_name: str,
        workflow_type: str,
        context: Dict = None
    ) -> str:
        """
        Trigger a specific agent workflow

        Args:
            user_id: User ID
            agent_name: Name of agent to trigger
            workflow_type: Type of workflow (analyze, plan, report, etc.)
            context: Additional context for the workflow

        Returns:
            Workflow output
        """
        workflow_prompts = {
            "analyze": "Please analyze the current situation and provide recommendations.",
            "plan": "Please create a detailed plan for moving forward.",
            "report": "Please provide a status report on current activities.",
            "brainstorm": "Please help me brainstorm ideas and approaches.",
            "review": "Please review the current state and suggest improvements."
        }

        base_prompt = workflow_prompts.get(workflow_type, "Please assist with this request.")

        if context:
            base_prompt += f"\n\nContext: {context}"

        response = self.agent_handler.process_message(
            user_id=user_id,
            message=base_prompt,
            agent_name=agent_name
        )

        return response

    def get_agent_status(self, agent_name: str) -> Dict:
        """
        Get status of an agent (output files, last activity, etc.)

        Args:
            agent_name: Name of agent

        Returns:
            Status information
        """
        try:
            # Find agent directory
            base_dir = Path(__file__).parent.parent
            agent_dirs = [
                base_dir / "Personal Agents" / agent_name,
                base_dir / "Team Agents" / agent_name,
                base_dir / "Worker Agents" / agent_name,
                base_dir / "Expert Agents" / agent_name,
            ]

            agent_dir = None
            for dir_path in agent_dirs:
                if dir_path.exists():
                    agent_dir = dir_path
                    break

            if not agent_dir:
                return {"error": f"Agent {agent_name} not found"}

            # Get output files
            output_dir = agent_dir / "Output"
            output_files = []

            if output_dir.exists():
                for file_path in sorted(output_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True):
                    if file_path.is_file():
                        output_files.append({
                            "name": file_path.name,
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })

            return {
                "agent_name": agent_name,
                "agent_dir": str(agent_dir),
                "output_files": output_files[:5],  # Last 5 files
                "total_outputs": len(output_files)
            }

        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {"error": str(e)}

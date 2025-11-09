"""
Goal Commands for Agent-Cleo Telegram Bot
Telegram interface for goal management
"""
import sys
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Add goal_helper to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Personal Agents" / "Coach-Cleo" / "Context"))


class GoalCommands:
    """Handles goal-related commands for Telegram"""

    def __init__(self):
        """Initialize GoalCommands"""
        pass

    def format_goal(self, goal: Dict, index: int = None) -> str:
        """Format a single goal for display"""
        priority_labels = {
            1: "📍 Weekly Goal",
            2: "🎯 Short Term Goal",
            3: "🌟 Long Term Goal",
            4: "💭 Someday Goal"
        }

        prefix = f"{index}. " if index else ""
        priority_label = priority_labels.get(goal.get('priority', 2), "Goal")

        # Get due date
        due_date = goal.get('due')
        if due_date:
            if isinstance(due_date, dict):
                due_str = due_date.get('date', 'Not set')
            else:
                due_str = str(due_date)
            due_text = f" | Due: {due_str}"
        else:
            due_text = ""

        # Completion status
        status = "✅" if goal.get('is_completed') else "⏸️"

        return f"{prefix}{status} {priority_label}: {goal['content']}{due_text}"

    def show_all_goals(self) -> str:
        """Show all goals organized by priority"""
        try:
            from goal_helper import (
                get_weekly_goals,
                get_short_term_goals,
                get_long_term_goals,
                get_someday_goals,
                get_active_weekly_goals,
                calculate_weekly_completion_rate
            )

            weekly = get_weekly_goals()
            active_weekly = get_active_weekly_goals()
            short_term = get_short_term_goals()
            long_term = get_long_term_goals()
            someday = get_someday_goals()
            completion_rate = calculate_weekly_completion_rate()

            response = f"""**Your Goals Overview**

**📍 Weekly Goals** ({len(active_weekly)} active)
Completion Rate: {completion_rate}%
"""
            if active_weekly:
                for i, goal in enumerate(active_weekly, 1):
                    response += f"\n{self.format_goal(goal, i)}"
            else:
                response += "\nNo active weekly goals. Use /weekly_planning to set them!"

            if short_term:
                response += f"\n\n**🎯 Short Term Goals** ({len(short_term)})"
                for i, goal in enumerate(short_term[:5], 1):  # Show top 5
                    response += f"\n{self.format_goal(goal, i)}"
                if len(short_term) > 5:
                    response += f"\n...and {len(short_term) - 5} more"

            if long_term:
                response += f"\n\n**🌟 Long Term Goals** ({len(long_term)})"
                for i, goal in enumerate(long_term, 1):
                    response += f"\n{self.format_goal(goal, i)}"

            if someday:
                response += f"\n\n**💭 Someday Goals** ({len(someday)})"
                response += f"\n{len(someday)} ideas captured for the future"

            return response

        except Exception as e:
            logger.error(f"Error showing goals: {e}", exc_info=True)
            return f"Error loading goals: {str(e)}\n\nMake sure goal_helper.py is properly configured."

    def show_weekly_goals(self) -> str:
        """Show weekly goals only"""
        try:
            from goal_helper import (
                get_active_weekly_goals,
                get_completed_weekly_goals,
                calculate_weekly_completion_rate
            )

            active = get_active_weekly_goals()
            completed = get_completed_weekly_goals()
            rate = calculate_weekly_completion_rate()

            response = f"""**📍 Weekly Goals**

**Active Goals ({len(active)}):**
"""
            if active:
                for i, goal in enumerate(active, 1):
                    due_date = goal.get('due', {})
                    due_str = due_date.get('date', 'Not set') if isinstance(due_date, dict) else due_date
                    response += f"\n{i}. {goal['content']}"
                    response += f"\n   Due: {due_str}"
                    response += f"\n   ID: {goal.get('id', 'N/A')[:8]}\n"
            else:
                response += "\nNo active weekly goals.\n"

            if completed:
                response += f"\n**Completed This Week ({len(completed)}):**\n"
                for goal in completed[:3]:  # Show last 3 completed
                    response += f"✅ {goal['content']}\n"

            response += f"\n**Completion Rate:** {rate}%"

            if rate >= 80:
                response += " 🎉 Excellent!"
            elif rate >= 60:
                response += " 💪 Good progress!"
            elif rate > 0:
                response += " 🎯 Keep pushing!"

            return response

        except Exception as e:
            logger.error(f"Error showing weekly goals: {e}", exc_info=True)
            return f"Error loading weekly goals: {str(e)}"

    def show_short_term_goals(self) -> str:
        """Show short term goals"""
        try:
            from goal_helper import get_short_term_goals

            goals = get_short_term_goals()

            response = f"""**🎯 Short Term Goals** ({len(goals)})

"""
            if goals:
                for i, goal in enumerate(goals, 1):
                    due_date = goal.get('due', {})
                    due_str = due_date.get('date', 'Not set') if isinstance(due_date, dict) else due_date
                    response += f"{i}. {goal['content']}\n"
                    response += f"   Due: {due_str}\n"
                    response += f"   ID: {goal.get('id', 'N/A')[:8]}\n\n"
            else:
                response += "No short term goals set.\n"
                response += "\nShort term goals are your quarterly/annual objectives that guide your weekly planning."

            return response

        except Exception as e:
            logger.error(f"Error showing short term goals: {e}", exc_info=True)
            return f"Error loading short term goals: {str(e)}"

    def show_long_term_goals(self) -> str:
        """Show long term goals"""
        try:
            from goal_helper import get_long_term_goals

            goals = get_long_term_goals()

            response = f"""**🌟 Long Term Goals** ({len(goals)})

"""
            if goals:
                for i, goal in enumerate(goals, 1):
                    response += f"{i}. {goal['content']}\n"
                    if goal.get('description'):
                        # Show first line of description
                        desc_lines = goal['description'].split('\n')
                        if desc_lines:
                            response += f"   {desc_lines[0][:60]}...\n"
                    response += f"   ID: {goal.get('id', 'N/A')[:8]}\n\n"
            else:
                response += "No long term goals set.\n"
                response += "\nLong term goals are your 3-5 year vision that guides your strategic direction."

            return response

        except Exception as e:
            logger.error(f"Error showing long term goals: {e}", exc_info=True)
            return f"Error loading long term goals: {str(e)}"

    def get_goal_stats(self) -> str:
        """Get goal statistics"""
        try:
            from goal_helper import (
                get_all_goals,
                get_weekly_goals,
                get_short_term_goals,
                get_long_term_goals,
                get_active_weekly_goals,
                calculate_weekly_completion_rate
            )

            all_goals = get_all_goals()
            weekly = get_weekly_goals()
            active_weekly = get_active_weekly_goals()
            short_term = get_short_term_goals()
            long_term = get_long_term_goals()
            completion_rate = calculate_weekly_completion_rate()

            completed_weekly = len(weekly) - len(active_weekly)

            response = f"""**📊 Goal Statistics**

**Overall:**
• Total Goals: {len(all_goals)}
• Long Term (3-5yr): {len(long_term)}
• Short Term (Quarterly): {len(short_term)}
• Weekly: {len(weekly)}

**This Week:**
• Active Weekly Goals: {len(active_weekly)}
• Completed: {completed_weekly}
• Completion Rate: {completion_rate}%

**Performance:**
"""
            if completion_rate >= 80:
                response += "🎉 Outstanding! You're crushing your goals!"
            elif completion_rate >= 60:
                response += "💪 Good work! Keep the momentum going!"
            elif completion_rate >= 40:
                response += "📈 Making progress. Focus on finishing!"
            elif completion_rate > 0:
                response += "🎯 Get focused. Finish what you started!"
            else:
                response += "⚠️ Time to set some weekly goals! Use /weekly_planning"

            return response

        except Exception as e:
            logger.error(f"Error getting goal stats: {e}", exc_info=True)
            return f"Error loading goal statistics: {str(e)}"

    def create_weekly_goal(self, goal_text: str) -> str:
        """
        Create a new weekly goal

        Args:
            goal_text: Goal description

        Returns:
            Success/error message
        """
        try:
            from goal_helper import create_weekly_goal, get_next_friday

            friday = get_next_friday()
            result = create_weekly_goal(
                content=goal_text,
                due_date=friday
            )

            if result.get('success'):
                return f"""✅ **Weekly Goal Created!**

{goal_text}

Due: Friday ({friday})
Project: {result.get('project', 'Personal')}

This goal has been added to your weekly commitments. Make sure it supports a Short Term Goal!"""
            else:
                return f"❌ Failed to create goal: {result.get('error', 'Unknown error')}"

        except Exception as e:
            logger.error(f"Error creating weekly goal: {e}", exc_info=True)
            return f"Error creating weekly goal: {str(e)}"

    def get_focus_recommendation(self) -> str:
        """Get the ONE thing to focus on today"""
        try:
            from goal_helper import get_active_weekly_goals

            active = get_active_weekly_goals()

            if not active:
                return "You don't have any active Weekly Goals. Use /weekly_planning to set your focus for the week!"

            # Sort by due date and priority
            def goal_priority(goal):
                due_date = goal.get('due', {})
                if isinstance(due_date, dict):
                    due_str = due_date.get('date', '9999-12-31')
                else:
                    due_str = str(due_date) if due_date else '9999-12-31'
                return (due_str, goal.get('priority', 2))

            sorted_goals = sorted(active, key=goal_priority)

            top_goal = sorted_goals[0]

            response = f"""**🎯 Your ONE Thing Today**

**Focus on:** {top_goal['content']}

"""
            due_date = top_goal.get('due', {})
            due_str = due_date.get('date', 'Not set') if isinstance(due_date, dict) else due_date
            response += f"Due: {due_str}\n"

            response += f"\n**Other Active Goals ({len(active) - 1}):**\n"
            for goal in sorted_goals[1:4]:  # Show next 3
                response += f"• {goal['content']}\n"

            if len(active) > 4:
                response += f"...and {len(active) - 4} more\n"

            response += "\n💡 **Tip:** Complete one goal at a time. Finish before you start something new!"

            return response

        except Exception as e:
            logger.error(f"Error getting focus recommendation: {e}", exc_info=True)
            return f"Error: {str(e)}"

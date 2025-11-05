"""
Goal Helper Functions for Coach-Cleo
Utility functions to read and work with goals from Todoist
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from todoist_integration import get_tasks_by_label, create_task_for_andrew


def get_next_friday():
    """
    Calculate the date of the next Friday (or today if today is Friday)

    Returns:
        String date in YYYY-MM-DD format
    """
    today = datetime.now()
    # Friday is weekday 4 (0=Monday, 6=Sunday)
    days_until_friday = (4 - today.weekday()) % 7

    # If today is Friday, use today; otherwise calculate next Friday
    if days_until_friday == 0 and today.weekday() == 4:
        next_friday = today
    elif days_until_friday == 0:
        next_friday = today + timedelta(days=7)
    else:
        next_friday = today + timedelta(days=days_until_friday)

    return next_friday.strftime("%Y-%m-%d")


def get_all_goals():
    """Get all goals with Agent-Cleo-Goals label"""
    return get_tasks_by_label("Agent-Cleo-Goals")


def get_goals_by_priority(priority: int):
    """
    Get goals by priority level

    Args:
        priority: 1=Weekly, 2=Short Term, 3=Long Term, 4=Someday

    Returns:
        List of goals at that priority level
    """
    all_goals = get_all_goals()
    return [g for g in all_goals if g['priority'] == priority]


def get_weekly_goals():
    """Get all Weekly Goals (Priority 1)"""
    return get_goals_by_priority(1)


def get_short_term_goals():
    """Get all Short Term Goals (Priority 2)"""
    return get_goals_by_priority(2)


def get_long_term_goals():
    """Get all Long Term Goals (Priority 3)"""
    return get_goals_by_priority(3)


def get_someday_goals():
    """Get all Someday Goals (Priority 4)"""
    return get_goals_by_priority(4)


def get_active_weekly_goals():
    """Get incomplete Weekly Goals"""
    weekly = get_weekly_goals()
    return [g for g in weekly if not g['is_completed']]


def get_completed_weekly_goals():
    """Get completed Weekly Goals"""
    weekly = get_weekly_goals()
    return [g for g in weekly if g['is_completed']]


def create_weekly_goal(content: str, due_date: str = None, supporting_goal: str = None):
    """
    Create a new Weekly Goal

    Weekly Goals are ALWAYS due on Friday of the current week.

    Args:
        content: Goal description
        due_date: Due date (optional - defaults to next Friday)
        supporting_goal: Which Short Term Goal this supports

    Returns:
        Result dictionary
    """
    # Weekly Goals always due Friday - if no date provided, use next Friday
    if due_date is None:
        due_date = get_next_friday()

    description = ""
    if supporting_goal:
        description = f"Supports Short Term Goal: {supporting_goal}\n\n"

    description += f"Weekly Goal - Due Friday {due_date}\n\n"

    return create_task_for_andrew(
        content=content,
        description=description,
        project="Personal",
        priority=1,  # Weekly Goal = Priority 1 (Urgent)
        due=due_date,
        labels=["Agent-Cleo-Goals"],
        agent="Coach-Cleo"
    )


def create_short_term_goal(content: str, due_date: str, supporting_goal: str = None):
    """
    Create a new Short Term Goal (Quarterly/Annual)

    Args:
        content: Goal description
        due_date: Due date (YYYY-MM-DD or quarter end)
        supporting_goal: Which Long Term Goal this supports

    Returns:
        Result dictionary
    """
    description = ""
    if supporting_goal:
        description = f"Supports Long Term Goal: {supporting_goal}\n\n"

    return create_task_for_andrew(
        content=content,
        description=description,
        project="Personal",
        priority=2,  # Short Term = Priority 2 (High)
        due=due_date,
        labels=["Agent-Cleo-Goals", "strategic"],
        agent="Coach-Cleo"
    )


def create_long_term_goal(content: str, vision: str = ""):
    """
    Create a new Long Term Goal (3-5 years)

    Args:
        content: Goal description
        vision: Description of the vision/outcome

    Returns:
        Result dictionary
    """
    description = f"3-5 Year Vision\n\n{vision}" if vision else "3-5 Year Goal"

    return create_task_for_andrew(
        content=content,
        description=description,
        project="Personal",
        priority=3,  # Long Term = Priority 3 (Medium)
        due=None,  # No specific due date
        labels=["Agent-Cleo-Goals", "vision"],
        agent="Coach-Cleo"
    )


def create_someday_goal(content: str, notes: str = ""):
    """
    Create a new Someday Goal

    Args:
        content: Goal description
        notes: Additional notes or thoughts

    Returns:
        Result dictionary
    """
    description = f"Someday/Maybe\n\n{notes}" if notes else "Someday Goal"

    return create_task_for_andrew(
        content=content,
        description=description,
        project="Personal",
        priority=4,  # Someday = Priority 4 (Normal)
        due=None,  # No due date
        labels=["Agent-Cleo-Goals", "someday"],
        agent="Coach-Cleo"
    )


def print_goal_summary():
    """Print a summary of all goals"""
    all_goals = get_all_goals()
    weekly = get_weekly_goals()
    short_term = get_short_term_goals()
    long_term = get_long_term_goals()
    someday = get_someday_goals()

    active_weekly = [g for g in weekly if not g['is_completed']]

    print("=" * 60)
    print("GOAL SUMMARY")
    print("=" * 60)
    print()
    print(f"Total Goals: {len(all_goals)}")
    print()
    print(f"[P1] Weekly Goals: {len(active_weekly)} active, {len(weekly) - len(active_weekly)} completed")
    print(f"[P2] Short Term Goals: {len(short_term)}")
    print(f"[P3] Long Term Goals: {len(long_term)}")
    print(f"[P4] Someday Goals: {len(someday)}")
    print()

    if active_weekly:
        print("Active Weekly Goals:")
        for i, goal in enumerate(active_weekly, 1):
            print(f"  {i}. {goal['content']}")
            print(f"     Due: {goal['due']}")
        print()

    if short_term:
        print("Short Term Goals:")
        for i, goal in enumerate(short_term, 1):
            print(f"  {i}. {goal['content']}")
            if goal['due']:
                print(f"     Due: {goal['due']}")
        print()

    if long_term:
        print("Long Term Goals:")
        for i, goal in enumerate(long_term, 1):
            print(f"  {i}. {goal['content']}")
        print()


def calculate_weekly_completion_rate():
    """Calculate this week's goal completion rate"""
    weekly = get_weekly_goals()
    if not weekly:
        return 0

    completed = len([g for g in weekly if g['is_completed']])
    total = len(weekly)

    rate = (completed / total) * 100
    return round(rate, 1)


if __name__ == "__main__":
    # Run when script is executed directly
    print_goal_summary()

    rate = calculate_weekly_completion_rate()
    if rate > 0:
        print(f"Weekly Completion Rate: {rate}%")
        if rate >= 80:
            print("[SUCCESS] Excellent! Target achieved!")
        elif rate >= 60:
            print("[GOOD] Good progress, keep pushing!")
        else:
            print("[FOCUS] Let's focus on finishing what we started")

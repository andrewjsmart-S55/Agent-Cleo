#!/usr/bin/env python3
"""
Script to display tasks scheduled for tomorrow from Todoist
"""
from todoist_integration import get_tomorrow_tasks
from datetime import datetime, timedelta

def main():
    tomorrow = datetime.now() + timedelta(days=1)
    print(f'Tasks for Tomorrow ({tomorrow.strftime("%A, %B %d, %Y")})')
    print('=' * 60)

    tasks = get_tomorrow_tasks()

    if not tasks:
        print('\nNo tasks scheduled for tomorrow.')
        print('\nEnjoy your free day or plan some new tasks!')
    else:
        # Group by project
        by_project = {}
        for task in tasks:
            project = task['project']
            if project not in by_project:
                by_project[project] = []
            by_project[project].append(task)

        # Display by project
        for project, project_tasks in sorted(by_project.items()):
            print(f'\n📁 {project}')
            print('-' * 60)
            for task in project_tasks:
                priority_symbols = {1: '  ', 2: '🔵', 3: '🟡', 4: '🔴'}
                priority = priority_symbols.get(task['priority'], '  ')
                print(f'{priority} {task["content"]}')
                if task['labels']:
                    labels_str = ', '.join(task['labels'])
                    print(f'   Labels: {labels_str}')
                if task['description']:
                    desc_preview = task['description'][:80]
                    if len(task['description']) > 80:
                        desc_preview += '...'
                    print(f'   {desc_preview}')
                print()

        print(f'\nTotal: {len(tasks)} task(s) for tomorrow')
        print('\nPriority Legend: 🔴 Urgent | 🟡 High | 🔵 Medium')

if __name__ == "__main__":
    main()

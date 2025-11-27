#!/usr/bin/env python3
"""
Entry point for the task management application
"""
from task_manager.ui import TaskManagerUI


def main():
    """Launch the application"""
    ui = TaskManagerUI()
    ui.run()


if __name__ == "__main__":
    main()

"""
User interface for task management
"""
from task_manager.models import Task, Priority
from task_manager.storage import TaskStorage


class TaskManagerUI:
    """Console interface for task management"""
    
    def __init__(self):
        self.storage = TaskStorage()
    
    def run(self):
        """Run the main application loop"""
        while True:
            self.show_menu()
            choice = input("\nSelect action: ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.mark_task_completed()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.show_statistics()
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
    
    def show_menu(self):
        """Show main menu"""
        print("\n" + "="*50)
        print("TASK MANAGER")
        print("="*50)
        print("1. Add task")
        print("2. Show tasks")
        print("3. Mark task as completed")
        print("4. Delete task")
        print("5. Statistics")
        print("0. Exit")
        print("="*50)
    
    def add_task(self):
        """Add new task"""
        print("\n--- New task ---")
        title = input("Title: ").strip()
        if not title:
            print("Title cannot be empty!")
            return
        
        description = input("Description: ").strip()
        
        print("\nPriority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Urgent")
        priority_choice = input("Select priority (1-4): ").strip()
        
        priority_map = {
            '1': Priority.LOW,
            '2': Priority.MEDIUM,
            '3': Priority.HIGH,
            '4': Priority.URGENT
        }
        priority = priority_map.get(priority_choice, Priority.MEDIUM)
        
        task = Task(id=0, title=title, description=description, priority=priority)
        self.storage.add_task(task)
        print(f"\n✓ Task '{title}' added!")
    
    def list_tasks(self):
        """Show task list"""
        print("\n--- Task list ---")
        tasks = self.storage.get_all_tasks()
        
        if not tasks:
            print("No tasks.")
            return
        
        for task in tasks:
            status = "✓" if task.completed else "○"
            priority_symbol = "!" * task.priority.value
            print(f"{status} [{task.id}] {priority_symbol} {task.title}")
            print(f"   {task.description}")
            print(f"   Priority: {task.priority.name}")
            print()
    
    def mark_task_completed(self):
        """Mark task as completed"""
        try:
            task_id = int(input("\nEnter task ID: "))
            task = self.storage.get_task(task_id)
            
            if task:
                if task.completed:
                    print("Task already completed!")
                else:
                    task.mark_completed()
                    self.storage.update_task(task)
                    print(f"✓ Task '{task.title}' marked as completed!")
            else:
                print("Task not found!")
        except ValueError:
            print("Invalid ID!")
    
    def delete_task(self):
        """Delete task"""
        try:
            task_id = int(input("\nEnter task ID to delete: "))
            task = self.storage.get_task(task_id)
            
            if task:
                confirm = input(f"Delete task '{task.title}'? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    self.storage.delete_task(task_id)
                    print("✓ Task deleted!")
                else:
                    print("Cancelled.")
            else:
                print("Task not found!")
        except ValueError:
            print("Invalid ID!")
    
    def show_statistics(self):
        """Show statistics"""
        all_tasks = self.storage.get_all_tasks()
        completed = self.storage.get_completed_tasks()
        incomplete = self.storage.get_incomplete_tasks()
        
        print("\n--- Statistics ---")
        print(f"Total tasks: {len(all_tasks)}")
        print(f"Completed: {len(completed)}")
        print(f"Incomplete: {len(incomplete)}")
        
        if all_tasks:
            completion_rate = (len(completed) / len(all_tasks)) * 100
            print(f"Completion rate: {completion_rate:.1f}%")

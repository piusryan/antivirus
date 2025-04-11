import os

class RamBooster:
    def __init__(self, task_list=None):
        """
        Initializes the RamBooster class with a list of tasks to terminate.
        :param task_list: List of process names to kill.
        """
        self.task_list = task_list if task_list else []

    def add_task(self, task_name):
        """
        Adds a task to the list of tasks to terminate.
        :param task_name: Name of the process (e.g., 'notepad.exe').
        """
        self.task_list.append(task_name)

    def kill_tasks(self):
        """
        Terminates all tasks in the task list.
        """
        for task in self.task_list:
            print(f"Attempting to kill: {task}")
            result = os.system(f"taskkill /f /im {task}")
            if result == 0:
                print(f"Successfully terminated {task}")
            else:
                print(f"Failed to terminate {task}. It might not be running.")

""" 
This module contain classes and methods related to CLI (Command Line Interface)
- Windows Only
"""
import csv
import subprocess



class TaskList:
    """
    Handles functions related to `tasklist` command of windows OS
    """
    
    def __init__(self) -> None:
        """
        Handles functions related to `tasklist` command of windows OS
        """
        # Args
        self.__tasksStr: str = ''
        self.__runningTasks: list[dict[str, str]] = []

        # Populate the args
        self._populate_tasks_str()
        self._populate_running_tasks()
    
    def _populate_running_tasks(self):
        """
        Populate `self.__runningTasks` after parsing data from `self.__tasksStr`, for all running tasks
        - Do not call this function directly
        """
        # Get data
        tasksList = self.__tasksStr.splitlines()
        
        # [Modify] Sorting tasksList & putting header on top
        header = tasksList[0]
        tasksList.remove(header)
        tasksList = sorted(tasksList)
        tasksList.insert(0, header)
        
        # Parsing data into a list[dict]
        csvR = csv.DictReader(tasksList)
        allTasks: list[dict[str, str]] = list(csvR)
        self.__runningTasks = allTasks
    
    def _populate_tasks_str(self):
        """
        Populate `self.__tasksStr` from the output of cmd.exe, for all running tasks
        - Do not call this function directly
        """
        self.__tasksStr = subprocess.check_output(
            'tasklist /fi "STATUS eq running" /fo "CSV"', 
            universal_newlines=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        ).strip()
    
    
    def get_headers(self):
        if not self.__runningTasks:
            return []
        task = self.__runningTasks[0]
        return list(task.keys())
    
    def get_task_instances(self, taskValue: str, key='Image Name'):
        """
        Returns a list of all instances of running tasks, 
        based on the `key = taskValue`
        """
        instances = []
        for i in self.__runningTasks:
            iValue = i.get(key)
            if iValue:
                iValue = iValue.lower()
            if iValue == taskValue.lower():
                instances.append(i)
        return instances

    def get_running_exes(self):
        """
        Returns a list of running executables
        """
        runningExes: list[str] = []
        for task in self.__runningTasks:
            exe = task.get('Image Name', 'None')
            runningExes.append(exe)
        return runningExes
    
    def get_running_tasks(self):
        """
        Returns a list of all running tasks (exe), as a dict, 
        with all available data like `Image Name`, `PID`, `Memory Usage` e.t.c
        - `[{...}, {...}, ...]`
        """
        return self.__runningTasks
    
    def is_exe_running(self, exe: str):
        """
        Returns `True` if executable of name `exe` is currently running
        """
        return exe.lower() in [
            i.lower() for i in self.get_running_exes()
        ]




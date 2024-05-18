""" 
This module contain classes and methods related to CLI (Command Line Interface)
- Windows Only
"""
import csv
from logging import Logger
import subprocess
from typing import Literal

from ._utils import _get_basic_logger
from .decorator import platform_specific




@platform_specific('win32')
class Attrib:
    """
    Handles the `attrib` command from windows OS.
    To set/modify/remove the `A/H/I/R/S` attributes for files/folders.
    Use `attrib /?` in CMD for more info.
    
    Args:
        - `path`: Path of the file/folder
    """

    def __init__(self, path:str) -> None:
        self.__path = path
        self.__attrsType = {
            'A':False,
            'H':False,
            'I':False,
            'R':False,
            'S':False
        }
    
    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self, 'path'
        )
    
    @property
    def path(self):
        """ Path of the file/folder for which attributes are being modified """
        return self.__path
    
    def set(
        self,
        a: bool | None = None,
        h: bool | None = None,
        i: bool | None = None,
        r: bool | None = None,
        s: bool | None = None
    ):
        """ Set attributes to the file/folder of `path` """
        # Data
        newAttrs = []
        currentAttrs = self.get()
        for x, y in zip(
            [a, h, i, r, s],
            self.__attrsType
        ):                                                                          # Collect: if not already set
            if x == True and not currentAttrs[y]:
                newAttrs.append(f'+{y}')
            elif x == False and currentAttrs[y]:
                newAttrs.append(f'-{y}')
        
        # Set attributes
        if newAttrs:
            newAttrs.insert(0,'attrib')
            newAttrs.append(self.__path)
            return subprocess.run(
                newAttrs, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )

    def get(self):
        """ Returns: Attributes set to the `path` """
        # Get attribs for path
        output = subprocess.check_output(
            [
                'attrib', self.__path
            ], 
            universal_newlines=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        currentAttribs = output[:9].replace(' ', '')
        
        # Parse the attribs
        attribs = dict(self.__attrsType)
        for i in currentAttribs:
            if i in attribs:
                attribs[i] = True
        return attribs




@platform_specific('win32')
class ICACLS:
    """
    Handles the `icacls` command from windows OS.
    To set/modify/remove the permissions for files/folders.
    Use `icacls /?` in CMD for more info.
    
    - Simple Permissions
        - N - no access
        - F - full access
        - M - modify access
        - RX - read and execute access
        - R - read-only access
        - W - write-only access
        - D - delete access
    
    Args:
        - `path`: Path of the file/folder
        - `accountName`: Name of the account for the processes (like modifying the permissions)
        - `logger`: `logging.Logger` to handle the logging
    """
    
    def __init__(
        self,
        path: str,
        accountName: str = 'Everyone',
        logger: Logger | None = None
    ):
        # Args
        self.__path = path
        self.__accountName = accountName
        self.__logger = logger or _get_basic_logger()
        
        # Data
        self.__perms = ['N', 'F', 'M', 'RX', 'R', 'W', 'D']
    
    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self, 'path', 'accountName', 'logger'
        )
    
    @property
    def path(self):
        """ Path of the file/folder for which permissions are being modified """
        return self.__path
    
    @property
    def accountName(self):
        """ Name of the account for which permissions are being modified """
        return self.__accountName
    
    @property
    def logger(self):
        """ `logging.Logger` being used for logging """
        return self.__logger
    
    @logger.setter
    def logger(self, value: Logger):
        self.__logger = value
    
    def _subprocessWrapper(
        self, 
        act: Literal['get', 'grant', 'deny', 'remove'], 
        perm: str | None = None
    ):
        """ Wrapper """
        if perm in self.__perms or act in ['get', 'remove']:
            # Permissions to set
            if act in ['get', 'remove']: 
                perm = None
            permToSet = f':(OI)(CI){perm}' if perm else ''

            # Command to run
            args = ['icacls', self.__path]
            if act != 'get':
                args += [
                    f'/{act}',
                    f'{self.__accountName}{permToSet}'
                ]
            
            # Process
            try:
                # icacls "B:/desktop/test" /deny Everyone:(OI)(CI)F
                return subprocess.check_output(
                    args,
                    universal_newlines=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except subprocess.CalledProcessError as e:
                self.__logger.error(f'{e}')
        else:
            self.__logger.info(f'Permission you want to set is not allowed ({perm})')

    def denyPermissions(self, perm:str='F'):
        """ Deny Permissions """ 
        # Permission
        permToCheck = '(N)' if perm=='F' else f'(DENY)({perm})'
        
        # Check if already set
        for i, v  in self.getInfo().items():
            if self.__accountName in i and permToCheck in v:
                return
        
        # If not running
        return self._subprocessWrapper(
            'deny', perm
        )
    
    def getInfo(self):
        """ 
        Return the ACL information about `path` 
        """
        output = self._subprocessWrapper('get')
        
        # Parsing output
        infoDict :dict[str, str] = {}
        if output:
            # Remove useless items
            output = output.removeprefix(self.__path)
            output = output.replace('  ', '').strip()
            
            # Data structure
            for p, i in enumerate(output.splitlines(), start=1):
                try: 
                    x, y = i.split(':')
                except ValueError:
                    pass
                else:
                    infoDict.update(
                        {
                            f'{p}- {x}': y
                        }
                    )
        
        return infoDict

    def grantPermissions(self, perm:str='F'):
        """ Grant Permissions """ 
        return self._subprocessWrapper(
            'grant', perm
        )

    def removeUser(self):
        """ Removes the `accountName` from file security """        
        return self._subprocessWrapper(
            'remove'
        )
    



@platform_specific('win32')
class TaskList:
    """
    Handles functions related to `tasklist` command of windows OS
    """
    
    def __init__(self):
        # Args
        self.__tasksStr: str = ''
        self.__runningTasks: list[dict[str, str]] = []

        # Populate the args
        self._populate_tasks_str()
        self._populate_running_tasks()
    
    def __str__(self) -> str:
        return self.get_formatted_str_representation()
    
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
    
    
    def get_formatted_str_representation(self):
        """
        Returns properly formatted representation of all running tasks
        """
        tasks = f" {'-'* 51}\n"
        for task in self.__runningTasks:
            for k, v in task.items():
                tasks += f"|   {k:15} : {v:30}|\n"
            tasks += f" {'-'* 51}\n"
        return tasks
    
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




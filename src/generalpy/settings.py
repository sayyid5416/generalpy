""" This module contains classes and methods related to settings """
import os
import json
from pathlib import Path
from typing import Callable, Any




class Settings:
    """
    Class to handle all settings related aspect for an app
    """
    
    def __init__(
        self,
        default_settings: dict[str, Any], 
        settings_directory: str | None = None,
        settings_file_name: str = 'settings.json',
        hard_fetch: bool = False
    ):
        """ 
        Class to handle all settings related aspect for an app

        Args:
        - `default_settings`: Default settings to be used in case any setting is missing
        - `settings_directory`: Directory where settings file would be stored (default: current working directory)
        - `settings_file_name`: Name of the settings file
        - `hard_fetch`: For fetching settings from settings file on every `get` and `update` method
            - If setting file is modified, those changes will be fetched in app
            - In other words, settings from settings file would be priortised over settings in app memory
            - Keep it False, if you don't want this behavior
        """
        # Args
        self.default_settings = default_settings
        self.settings_directory = settings_directory if settings_directory else os.getcwd()
        self.settings_file_name = settings_file_name
        self.hard_fetch = hard_fetch                                                 # for hard-fetching settings from file (see docstring)
        
        # Init
        self.settings_file_path = self._get_settings_file_path()                     # path of settings file
        self._settings = self._load_settings()                                       # all settings

    @staticmethod
    def _hard_fetch(func: Callable):
        """ 
        Decorator to load settings from settings file before running decorated function 
        """
        def wrapper(self, *args, **kwargs):
            if self.hard_fetch:
                self._settings = self._load_settings()
            return func(self, *args, **kwargs)
        return wrapper

    def _load_settings(self) -> dict[str, Any]:
        """ 
        Returns settings from settings file
        - Also handles if some or all settings missing or corrupted
        """
        # [Check] if settings file not present: Default settings
        if not Path(self.settings_file_path).is_file():
            self._save_settings(self.default_settings)
            return dict(self.default_settings)

        # [Load] settings from file
        with open(self.settings_file_path, 'r') as f:
            try:
                settings = json.load(f)
                # [Check] if all default settings are present in file
                for key in self.default_settings:
                    if key not in settings:
                        settings[key] = self.default_settings[key]
                        self._save_settings(settings)
                return settings
            except json.decoder.JSONDecodeError:
                self._save_settings(self.default_settings)
                return dict(self.default_settings)

    def _save_settings(self, settings: dict[str, Any]) -> None:
        """ 
        Save the `setting` dict to settings file
        - Create file if not present
        """
        path = Path(self.settings_file_path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(self.settings_file_path, 'w') as f:
            json.dump(
                settings, f,
                indent=4,
                sort_keys=True
            )

    def _get_settings_file_path(self) -> str:
        """
        Create the settings file path by joining the settings directory and settings file name
        """
        return os.path.join(
            self.settings_directory,
            self.settings_file_name
        )

    @_hard_fetch
    def update_setting(self, key: str, value: Any) -> None:
        """ 
        Updates the setting `key` = `value` in settings file 
        """
        self._settings[key] = value
        self._save_settings(self._settings)

    @_hard_fetch
    def get_setting(self, key: str) -> Any | None:
        """ 
        Returns the value of setting `key` 
        """
        return self._settings.get(key)
    
    @_hard_fetch
    def get_all_settings(self) -> dict[str, Any]:
        """
        Returns all the settings 
        """
        return self._settings
    
    def reset(self):
        """ 
        Reset all settings in settings file
        - Overrite settings file with default settings 
        """
        self._settings = dict(self.default_settings)
        self._save_settings(self._settings)
    

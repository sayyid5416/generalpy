""" This module contains classes and methods useful for apps """
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
        settings_directory: str, 
        settings_file_name: str = 'settings.json',
        hard_refresh: bool = False
    ):
        """ 
        Class to handle all settings related aspect for an app

        Args:
        - `default_settings`: Default settings to be used in case any setting is missing
        - `settings_directory`: Directory where settings file would be stored
        - `settings_file_name`: Name of the settings file
        - `hard_refresh`: If `True`, settings would be refreshed on every `get` and `update` method from file (it's not really necessary)
        """
        # Args
        self.default_settings = default_settings
        self.settings_directory = settings_directory
        self.settings_file_name = settings_file_name
        self.hard_refresh = hard_refresh
        
        # Init
        self.settings_file_path = self.get_settings_file_path()
        self.settings = self._load_settings()

    @staticmethod
    def _D_refresh_settings(func: Callable):
        """ 
        Decorator to load settings before running decorated function 
        """
        def wrapper(self, *args, **kwargs):
            if self.hard_refresh:
                self.settings = self._load_settings()
            return func(self, *args, **kwargs)
        return wrapper

    def _load_settings(self) -> dict[str, Any]:
        """ 
        Returns settings from settings file
        - Also handles if some or all settings missing 
        """
        # [Check] if settings file not present: Default settings
        if not Path(self.settings_file_path).is_file():
            self._save_settings(self.default_settings)
            return self.default_settings

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
                return self.default_settings

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

    @_D_refresh_settings
    def update_setting(self, key: str, value: Any) -> None:
        """ 
        Updates the setting `key` = `value` in settings file 
        """
        self.settings[key] = value
        self._save_settings(self.settings)

    @_D_refresh_settings
    def get_setting(self, key: str) -> Any | None:
        """ 
        Returns the value of setting `key` 
        """
        return self.settings.get(key)
    
    @_D_refresh_settings
    def get_all_settings(self) -> dict[str, Any]:
        """
        Returns all the settings 
        """
        return self.settings
    
    def get_settings_file_path(self) -> str:
        """
        Create the settings file path by joining the settings directory and settings file name
        """
        return os.path.join(
            self.settings_directory,
            self.settings_file_name
        )

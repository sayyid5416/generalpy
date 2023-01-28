"""
This module contains classes and methods related to settings
"""
import json
import os
from pathlib import Path
from typing import Callable, Any

"""
Items imported inside functions/classes

- from .general import generate_repr_str
"""




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
            - `hard_fetch`: If `True`, Fetches settings from settings file on every `get`, `update` and `__init__` method,
                otherwise settings will be loaded from settings file only on `__init__` of this class.
        
        Handling missing settings from settings file:
            - Settings file will be updated with missing data on: 
                - every `fetching` of settings from settings file (d/f behavior acc. to `hard_fetch`)
                - on `update`
                - on `reset`
        
        Handling if settings file was modified: 
            - Settings would be fetched from settings-file on:
                - every `fetching` of settings from settings file (d/f behavior acc. to `hard_fetch`)
        """
        # Args
        self.default_settings = default_settings
        self.settings_directory = settings_directory if settings_directory else os.getcwd()
        self.settings_file_name = settings_file_name
        self.hard_fetch = hard_fetch                                                 # for hard-fetching settings from file (see docstring)
        
        # Init
        self.settings_file_path = self._get_settings_file_path()                     # path of settings file
        self._settings = self._load_settings()                                       # all settings

    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self, 'default_settings', 'settings_directory', 'settings_file_name', 'hard_fetch'
        )
    
    def __str__(self) -> str:
        """ Returns all settings in a properly formatted string """
        if not self._settings:
            return 'No settings available'
        
        text = 'Current settings:\n'
        for k, v in self._settings.items():
            text += f'• {k:20} : {v}\n'
        return text.strip()

    def _get_settings_file_path(self) -> str:
        """
        Create the settings file path by joining the settings directory and settings file name
        """
        return os.path.join(
            self.settings_directory,
            self.settings_file_name
        )

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

    @staticmethod
    def _reload_settings(func: Callable):
        """
        Decorator to re-load settings from settings-file 
        before running the decorated function 
        """
        def wrapper(self, *args, **kwargs):
            if self.hard_fetch:
                self._settings = self._load_settings()
            return func(self, *args, **kwargs)
        return wrapper

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

    @_reload_settings
    def get_setting(self, key: str, default: Any | None = None):
        """ 
        Returns the value of setting `key`.
        - Returns `default`, if setting not found
        """
        return self._settings.get(key, default)
    
    @_reload_settings
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
    
    @_reload_settings
    def update_setting(self, key: str, value: Any) -> None:
        """ 
        Updates the setting `key` = `value` in settings file 
        """
        self._settings[key] = value
        self._save_settings(self._settings)

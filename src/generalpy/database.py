"""
This module contain classes and methods related to database/settings handling
"""
import json
import os
from pathlib import Path
from typing import Any, Callable

"""
Items imported inside functions/classes
- from .general import generate_repr_str
"""





class DatabaseCollection:
    """
    - Handles the data of a collection `collectionName` in some database.
    - This database will be in memory, but you can extend this functionality by using this class as a base class.
    - Database structure should be: `DataBase > collection > collection-data`.
    
    Args:
        - `collectionName`                  : Name of the collection in database
        - `initialData`                     : Initial data present in the collection (on initiation)
        - `_delete_dataID_fctn(dataID)`                          : It will run (in last), when `delete_data_of_dataID` is called.
        - `_delete_dataType_fctn(dataID, dataType)`              : It will run (in last), when `delete_data_of_dataType` is called.
        - `_update_dataID_fctn(dataID, dataValue)`               : It will run (in last), when `update_data_of_dataID` is called.
        - `_update_dataType_fctn(dataID, dataType, dataValue)`   : It will run (in last), when `update_data_of_dataType` is called.
    
    Structure of `collection-data` (`dict[str, dict[str, Any]]`) :
    ```python
    {
        dataID_1 (str) : {
            dataType_1 (str): dataValue_1 (Any),
            dataType_2 (str): dataValue_2 (Any),
            ...
        },
        dataID_2: {
            dataType_1: dataValue_1,
            dataType_2: dataValue_2,
            ...
        },
        ...        
    }
    ```
    """
    
    def __init__(
        self,
        collectionName: str,
        initialData: dict[str, dict[str, Any]] | None = None,
        _delete_dataID_fctn:     Callable[[str], Any] =                  lambda *args, **kwargs: None,
        _delete_dataType_fctn:   Callable[[str, str], Any] =             lambda *args, **kwargs: None,
        _update_dataID_fctn:     Callable[[str, dict[str, Any]], Any] =  lambda *args, **kwargs: None,
        _update_dataType_fctn:   Callable[[str, str, Any], Any] =        lambda *args, **kwargs: None,
    ):
        # Args
        self.collectionName = collectionName
        self.initialData = initialData if initialData else {}
        self._delete_dataID_fctn = _delete_dataID_fctn
        self._delete_dataType_fctn = _delete_dataType_fctn
        self._update_dataID_fctn = _update_dataID_fctn
        self._update_dataType_fctn = _update_dataType_fctn

        # Data in collection
        # {dataID : {dataType: dataValue, ...}, ... }
        self.__collectionData: dict[str, dict[str, Any]] = dict(self.initialData)
    
    def __repr__(self):
        from .general import generate_repr_str
        return generate_repr_str(
            self, 
            'collectionName', 
            'initialData',
            '_delete_dataID_fctn',
            '_delete_dataType_fctn',
            '_update_dataID_fctn',
            '_update_dataType_fctn',
        )
    
    def __str__(self):
        return 'JSON Representation of all data:\n' \
            + self.get_all_data_as_json()
    
    
    ## ----------------- Internal functions (for handling self.__collectionData) ----------------- ##
    def _get_collectionData(self):
        return self.__collectionData

    def _pop_from_collectionData(self, dataID: str):
        return self.__collectionData.pop(dataID)
    
    def _set_collectionData(self, collectionData: dict[str, dict[str, Any]]):
        self.__collectionData = collectionData

    def _update_collectionData(self, dataID: str, dataValue: dict[str, Any]):
        self.__collectionData.update(
            {dataID: dataValue}
        )
    

    ## ---------------------------------- Getting data ---------------------------------- ##
    def get_all_data(self):
        """
        Returns all data from the collection of database
        """
        return self._get_collectionData()
    
    def get_all_data_as_json(self, indent=4, sort=True):
        """
        Returns all data from the collection of database
        - as `json` string
        """
        return json.dumps(
            self.get_all_data(),
            indent=indent,
            sort_keys=sort
        )
    
    def get_data_of_dataID(
        self,
        dataID: str | int, 
        default: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Returns: data/value of `dataID` from collection
        - `default` will be returned, if data not found. 
        If `default=None`, empty dict would be returned.
        """
        # Modify data
        dataID = str(dataID)
        if default is None:
            default = {}
        
        # Return data of dataID from collection
        return self.get_all_data().get(
            dataID, default
        )
    
    def get_data_of_dataType(
        self,
        dataID: str | int,
        dataType: str | int,
        default: Any = None
    ) -> Any:
        """
        Returns: data/value of `dataType` from `dataID` from collection
        - `default` will be returned, if data not found
        """
        dataID = str(dataID)
        dataType = str(dataType)
        idData = self.get_data_of_dataID(dataID)
        return idData.get(
            dataType, default
        )


    ## ---------------------------------- Updating data ---------------------------------- ##
    def copy_data_of_dataID(
        self,
        oldDataID: str | int,
        newDataID: str | int,
        deleteOldID: bool = False
    ):
        """ 
        Copy all data from `oldDataID` to `newDataID`
        - `deleteOldID`: Deletes oldDataID from collection after copying
        """
        # Modify data
        oldDataID = str(oldDataID)
        newDataID = str(newDataID)
        
        # Data of old dataID
        idData = self.get_data_of_dataID(oldDataID)
        
        # Copying data to new dataID
        self.update_data_of_dataID(
            newDataID, dict(idData)
        )
        
        # Deleting old dataID
        if deleteOldID:
            self.delete_data_of_dataID(oldDataID)
    
    def delete_data_of_dataID(self, dataID: str|int):
        """
        Deletes the `dataID` and its data from collection
        """
        dataID = str(dataID)
        if dataID in self.get_all_data():
            self._pop_from_collectionData(dataID)
            self._delete_dataID_fctn(dataID)
    
    def delete_data_of_dataType(
        self,
        dataID: str | int,
        *dataTypes: str | int
    ):
        """
        Deletes the `dataType` and its data from `dataID` of collection
        """
        # Modify
        dataID = str(dataID)
        dataTypes = tuple(str(i) for i in dataTypes)

        # Delete dataType from dataID of collection
        idData = self.get_data_of_dataID(dataID)
        for dataType in dataTypes:
            if dataType in idData:
                idData.pop(dataType)
                self._delete_dataType_fctn(
                    dataID, dataType
                )
        
        # Update the new data of dataID
        self.update_data_of_dataID(
            dataID, idData
        )

    def update_data_of_dataID(
        self,
        dataID: str | int,
        dataValue: dict[str, Any]
    ):
        """
        Update the data of `dataID` with `dataValue`
        """
        dataID = str(dataID)
        self._update_collectionData(dataID, dataValue)
        self._update_dataID_fctn(dataID, dataValue)

    def update_data_of_dataType(
        self,
        dataID: str | int,
        dataType: str | int,
        dataValue: Any
    ):
        """
        Update the data of `dataType` (of `dataID`) with `dataValue`
        """
        # Modify data
        dataID = str(dataID)
        dataType = str(dataType)
        
        # Data of dataID (Get -> Update)
        idData = self.get_data_of_dataID(dataID)
        idData.update(
            {dataType: dataValue}
        )
        self._update_dataType_fctn(
            dataID, dataType, dataValue
        )
        
        # Update data of collection
        self.update_data_of_dataID(
            dataID, idData
        )





class Settings:
    """ 
    Class to handle all settings related aspect for an app

    Args:
        - `default_settings`: Settings to be used if any setting is missing
        - `settings_directory`: Directory to store settings-file (default: current directory)
        - `settings_file_name`: Name of the settings-file
        - `hard_fetch`: If `True`, Fetches settings from settings-file on every `get`, `update` and `__init__` method,
            otherwise settings will be loaded from settings-file only on `__init__` of this class.
    
    [Handling] If some settings are missing in settings-file:
        - Settings-file will be updated with missing data on: 
            - every `fetching` from settings-file (behaves acc. to `hard_fetch`)
            - on `update`
            - on `reset`
    
    [Handling] If settings-file was modified: 
        - Settings would be fetched from settings-file on:
            - every `fetching` from settings-file (behaves acc. to `hard_fetch`)
    """
    
    def __init__(
        self,
        default_settings: dict[str, Any], 
        settings_directory: str | None = None,
        settings_file_name: str = 'settings.json',
        hard_fetch: bool = False
    ):
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

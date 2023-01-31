"""
This module contain classes and methods related to database handling
"""
import json
from typing import Any, Callable





class DatabaseCollection:
    """
    - Handles the data of a collection `collectionName` in some database.
    - This database will be in memory, but you can extend this functionality by using this class as a base class.
    - Database structure should be: `DataBase > collection > collection-data`.
    
    Args:
    - `collectionName`                  : Name of the collection in database
    - `initialData`                     : Initial data present in the collection (on initiation)
    - `delete_dataID_fctn(dataID)`                          : It will run (in last), when `delete_data_of_dataID` is called.
    - `delete_dataType_fctn(dataID, dataType)`              : It will run (in last), when `delete_data_of_dataType` is called.
    - `update_dataID_fctn(dataID, dataValue)`               : It will run (in last), when `update_data_of_dataID` is called.
    - `update_dataType_fctn(dataID, dataType, dataValue)`   : It will run (in last), when `update_data_of_dataType` is called.
    
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
        _delete_dataID_fctn:     Callable[[str], ...] =                  lambda *args, **kwargs: None,
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

        # Data -> {dataID : {dataType: dataValue, ...}, ... }
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
        return 'JSON Representation of all data:\n' + self.get_all_data_as_json()
    
    
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
        dataID: str|int, 
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
        # Modify
        dataID = str(dataID)
        
        # Delete dataID from collection
        allData = self.get_all_data()
        if dataID in allData:
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
        # Modify data
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
    
    
    ## ----------------- Internal functions (for handling self.__collectionData) ----------------- ##
    def _get_collectionData(self):
        return self.__collectionData

    def _pop_from_collectionData(self, dataID: str):
        return self.__collectionData.pop(dataID)
    
    def _update_collectionData(self, dataID: str, dataValue: dict[str, Any]):
        self.__collectionData.update(
            {dataID: dataValue}
        )
    
    def _set_collectionData(self, collectionData: dict[str, dict[str, Any]]):
        self.__collectionData = collectionData




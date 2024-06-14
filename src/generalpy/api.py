"""
Module related to APIs and related functions
"""

import json
from logging import Logger
import requests

from .general import format_dict
from ._utils import _get_basic_logger






#-todo: async
class Api_Call:
    
    def __init__(
        self,
        baseUrl: str,
        apiKeyValue: tuple[str, str|None] | None,
        logger: Logger | None = None,
        **keyValuePairs,
    ):
        """
        Class to handle API calls.

        Args:
            baseUrl: The base URL for the API.
            apiKeyValue: A tuple containing the API key name and its value. If the value is None, it indicates no API key is required.
            logger: Logger instance for logging. If None, a basic logger will be created.
            **keyValuePairs: Additional key-value pairs to be included in the API request headers or parameters.
        """
        # Args
        self.__baseUrl = baseUrl
        self.__apiKeyValue = apiKeyValue
        self.__keyValuePairs = keyValuePairs
        self.__logger = logger or _get_basic_logger()
    
    @property
    def api_key(self):
        """ API `(key, value)` """
        return self.__apiKeyValue
    
    @property
    def apiUrl(self):
        """ URL endpoint to call the API """
        endpoint = self.__baseUrl + '?'
        if self.__keyValuePairs:
            for key, value in self.__keyValuePairs.items():
                if value is not None:
                    endpoint += f'&{key}={value}'
        if self.api_key:
            endpoint += f'&{self.api_key[0]}={self.api_key[1]}'
            
        return endpoint
        
    @property
    def apiResponse(self):
        """ Response from the API """
        response = requests.get(self.apiUrl)
        return response
    
    @property
    def apiResponseJson(self):
        """ JSON format of response from API """
        try:
            return self.apiResponse.json()
        except Exception as e:
            self.__logger.debug(e)
            return {
                'error': 'Invalid data',
                'detail': 'Unable to parse the return format. It seems like it is not a JSON response.'
            }

    def get_response_raw_str(self):
        """ Get str of properly formatted api response """
        return json.dumps(
            self.apiResponseJson,
            indent=4
        )
    
    def get_response_simple_str(self, data: dict=None):
        """
        Get str of properly formatted SIMPLISTIC api response
        - if `data` is provided -> It will be formatted and returned.
        - otherwise -> data will be taken from API
        """
        return format_dict(
            data or self.apiResponseJson,
            5,
            keyPrefix='• '
        )
    

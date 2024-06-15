"""
Module related to APIs and related functions
"""

import json
from logging import Logger
import requests

from .general import format_dict
from ._utils import _get_basic_logger






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
        - Contains both sync and async functions
        - async functions requires you to install aiohttp

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
            return self._return_invalid_data()

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

    
    ## ----------------------------------------- Async ----------------------------------------- ##
    @property
    async def async_apiResponseJson(self):
        """ (ASYNC) JSON format of response from API """
        try:
            return await self._async_get_response_json_from_url(self.apiUrl)
        except Exception as e:
            self.__logger.debug(e)
            return await self._async_return_invalid_data()

    async def async_get_response_raw_str(self):
        """ (ASYNC) Get str of properly formatted API response """
        responseJson = await self.async_apiResponseJson
        return json.dumps(responseJson, indent=4)

    async def async_get_response_simple_str(self, data: dict | None = None):
        """
        (ASYNC) Get str of properly formatted simplistic API response
        - if `data` is provided -> It will be formatted and returned.
        - otherwise -> data will be taken from API
        """
        if data is None:
            data = await self.async_apiResponseJson
        return format_dict(data, 5, keyPrefix='• ')


    ## ----------------------------------------- Internals ----------------------------------------- ##
    def _return_invalid_data(self):
        """ Returns invalid data dict """
        return {
            'code': '404',
            'error': 'Invalid data',
            'detail': 'Unable to parse the return format. It seems like it is not a JSON response.'
        }
    
    async def _async_return_invalid_data(self):
        """ Returns invalid data dict """
        return self._return_invalid_data()

    @staticmethod
    async def _async_get_response_json_from_url(url: str):
        """ (ASYNC) Response JSON from the API """
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

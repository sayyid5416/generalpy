""" 
This module contains classes and methods related to logging
"""
from bisect import bisect
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

from pytz import timezone

"""
Items imported inside functions/classes

- from .general import generate_repr_str
"""




class CustomLogging:
    """
    Class to handle logging in easy way
    
    Args:
    - `loggerName` : Name of the logger
    - `loggingLevel` : level of logging like `logging.INFO`, logging.`ERROR` etc
    - `allLogsFilePath` : If passed, all `INFO` level logs would be saved to this file (with full format)
    - `errorLogsFilePath` : If passed, all `ERROR` level logs would be saved to this file (with full format)
    - `timeZone` : time zone to set for `%(asctime)s` in full format
    - `compactStreamLogs` : Handle if stream logs should be compact or in full format
    - `initialMsg` : Initial message to set as soon as the logger initiates for the first time
    """
    
    compactFormat = f"%(module)-20s %(lineno)-4d : {' ' * 10} %(message)s"
    fullFormat = f"[%(levelname)-8s] [%(asctime)s]   %(lineno)-4d - %(module)-20s : {' ' * 10} %(message)-100s {' ' * 10} [%(threadName)s]"
    
    def __init__(
        self,
        loggerName: str | None = None,
        loggingLevel: int = logging.INFO,
        allLogsFilePath: str | None = None,
        errorLogsFilePath: str | None = None, 
        timeZone: str = 'Asia/Kolkata',
        compactStreamLogs: bool = True,
        initialMsg: str = ''
    ):
        # Args
        self.__loggerName = loggerName if loggerName else __name__
        self.__loggingLevel = loggingLevel
        self.__allLogsFilePath = allLogsFilePath
        self.__errorLogsFilePath = errorLogsFilePath
        self.__timeZone = timeZone
        self.__compactStreamLogs = compactStreamLogs
        self.__initialMsg = initialMsg
        
        # Variables
        self.__logger = self._initiate_logger()                                                   # Logger
        self.__handlers: set[logging.Handler] = set()                                             # List of all available handlers
        self.__compact_formatter = self._get_compact_formatter()
        self.__full_formatter = self._get_full_formatter()
        
        # Logging
        self._initiate_stream_logging()
        if self.__allLogsFilePath:
            self._initiate_file_logging(
                self.__allLogsFilePath, logging.INFO
            )
        if self.__errorLogsFilePath:
            self._initiate_file_logging(
                self.__errorLogsFilePath, logging.ERROR
            )
        if self.__initialMsg:
            self.raw_logging(
                self.__initialMsg, True, True
            )

    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self,
            'loggerName',
            'loggingLevel',
            'allLogsFilePath',
            'errorLogsFilePath',
            'timeZone',
            'compactStreamLogs',
            'initialMsg'
        )


    ## ----------------------- Properties ----------------------- ##
    @property
    def logger(self):
        """ main `logging.Logger` to be used for logging """
        return self.__logger
    
    @property
    def timeZone(self):
        """ timezone for the logging time """
        return self.__timeZone
    
    @property
    def compactStreamLogs(self):
        """ Are stream logs compact type """
        return self.__compactStreamLogs
    
    @property
    def allLogsFilePath(self):
        """ Path of the file which contains all logs """
        return self.__allLogsFilePath
    
    @property
    def errorLogsFilePath(self):
        """ Path of the file which contains error logs """
        return self.__errorLogsFilePath
    
    
    ## ----------------------- Main functions ----------------------- ##
    def close_logging_handlers(self):
        """ Close all available handlers: All file handlers & stream handler """
        for i in self.__handlers:
            i.close()

    def raw_logging(self, msg:str, toAllLogsFile=False, toErrorLogsFile=False):
        """ 
        Write Raw `msg` to appropriate logs (along with `terminal`) , without any formatting
        - toAllLogsFile : If `True`, `msg` would be logged to `allLogsFilePath` too (if setted in constructor) .
        - toAllLogs : If `True`, `msg` would be logged to `errorLogsFilePath` too (if setted in constructor) .
        """
        def write_to_file(filePath:str):
            with open(filePath, 'a') as f:
                f.write(
                    f'{msg}\n'
                )
        
        # Logging
        print(msg)
        if toAllLogsFile and self.__allLogsFilePath:
            write_to_file(self.__allLogsFilePath)
        if toErrorLogsFile and self.__errorLogsFilePath:
            write_to_file(self.__errorLogsFilePath)


    ## ----------------------- Internals ----------------------- ##
    def _add_handler(self, handler: logging.Handler):
        """ Adds `handler` to `Logger` """
        self.__logger.addHandler(handler)
        self.__handlers.add(handler)
    
    def _get_compact_formatter(self):
        """ Returns compact `Formatter` after initiating it for all levels """
        return LevelFormatter(
            {
                logging.DEBUG: f'~   {self.compactFormat}',
                logging.INFO: f'>   {self.compactFormat}',
                logging.WARNING: f'[!] {self.compactFormat}',
                logging.ERROR: f'[x] {self.compactFormat}',
            },
            timeZone=self.__timeZone
        )

    def _get_full_formatter(self):
        """ Returns full `Formatter` after initiating it for all levels """
        return LevelFormatter(
            {
                logging.DEBUG: f'~   {self.fullFormat}',
                logging.INFO: f'>   {self.fullFormat}',
                logging.WARNING: f'[!] {self.fullFormat}',
                logging.ERROR: f'[x] {self.fullFormat}',
            },
            datefmt=f"%Y-%m-%d %I:%M:%S %p ({self.__timeZone})",
            timeZone=self.__timeZone
        )
    
    def _initiate_file_logging(self, fileLocation:str, loggingLevel, formatter: logging.Formatter | None = None):
        """ Initiates logs streaming to file present at `fileLocation`
        - `loggingLevel`: Logging level to set for this file
        - `formatter`: Formatting for logs (default: `self.__full_formatter`)
        """
        if formatter is None:
            formatter = self.__full_formatter
        fileHand = RotatingFileHandler(
            fileLocation, 
            maxBytes=int(1024 * 1024),
            backupCount=1
        )
        fileHand.setFormatter(formatter)
        fileHand.setLevel(loggingLevel)
        self._add_handler(fileHand)
    
    def _initiate_logger(self):
        """ Returns `Logger` after initiating it """
        return logging.Logger(
            self.__loggerName,
            self.__loggingLevel
        )
    
    def _initiate_stream_logging(self):
        """ Initiates logs streaming to Terminal
        - `Formatter` is based on `self.__compactStreamLogs`
        """
        streamHand = logging.StreamHandler()
        streamHand.setFormatter(
            self.__compact_formatter if self.__compactStreamLogs else self.__full_formatter
        )
        self._add_handler(streamHand)






class LevelFormatter(logging.Formatter):
    """ `Formatter` class which sets formatting, based on the Levels, like `INFO`, `ERROR` etc 
    - `formats` (dict) : `{levelno: fmt, ...}`
    - `timeZone`: Change timezone for `%(asctime)s`
    """
    
    def __init__(self, formats: dict[int, str], timeZone: str = 'Asia/Kolkata', *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Args
        self.__formats = formats
        self.__args = args
        self.__kwargs = kwargs
        self.__timeZone = timeZone

        # Function
        if 'fmt' in self.__kwargs:
            raise ValueError('Keyword argument "fmt" deprecated, use "formats"')
        self.set_time_zone(self.__timeZone)
        self.__formatters = sorted(
            (
                levelno,
                logging.Formatter(
                    fmt, **self.__kwargs
                )
            ) for levelno, fmt in self.__formats.items()
        )
    
    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(self, 'formats', 'timeZone', 'args', 'kwargs')
    
    @property
    def timeZone(self):
        """ Timezone """
        return self.__timeZone
    
    def format(self, record: logging.LogRecord) -> str:
        """ Sets formatting """
        idx = bisect(
            a=self.__formatters,
            x=(record.levelno,),                                                   # Comma: To make it a tuple, instead of int
            hi=len(self.__formatters) - 1
        )
        levelno, formatter = self.__formatters[idx]
        return formatter.format(
            record
        )

    @staticmethod
    def set_time_zone(timeZone):
        """ Sets the timezone """
        logging.Formatter.converter = lambda *args: datetime.now(
            tz=timezone(timeZone)
        ).timetuple()


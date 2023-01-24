""" This module contains classes and methods related to logging """
import logging
from bisect import bisect
from datetime import datetime
from logging.handlers import RotatingFileHandler

from pytz import timezone



class LevelFormatter(logging.Formatter):
    
    def __init__(self, formats: dict[int, str], timeZone: str = 'Asia/Kolkata', *args, **kwargs):
        """ `Formatter` class which sets formatting, based on the Levels, like `INFO`, `ERROR` etc 
        - `formats` (dict) : `{levelno: fmt, ...}`
        - `timeZone`: Change timezone for `%(asctime)s`
        """
        super().__init__(*args, **kwargs)
        if 'fmt' in kwargs:
            raise ValueError('Keyword argument "fmt" deprecated, use "formats"')
        self.set_time_zone(timeZone)
        self.formats = sorted(
            (
                levelno,
                logging.Formatter(
                    fmt, **kwargs
                )
            ) for levelno, fmt in formats.items()
        )
    
    @staticmethod
    def set_time_zone(timeZone):
        """ Sets the timezone """
        logging.Formatter.converter = lambda *args: datetime.now(
            tz=timezone(timeZone)
        ).timetuple()

    def format(self, record: logging.LogRecord) -> str:
        """ Sets formatting """
        idx = bisect(
            a=self.formats,
            x=(record.levelno,),                                                   # Comma: To make it a tuple, instead of int
            hi=len(self.formats) - 1
        )
        levelno, formatter = self.formats[idx]
        return formatter.format(
            record
        )



class CustomLogging:
    """ Class to handle logging in easy way """
    
    def __init__(
        self,
        loggerName: str,
        loggingLevel: int = logging.INFO,
        allLogsFilePath: str | None = None,
        errorLogsFilePath: str | None = None, 
        timeZone: str = 'Asia/Kolkata',
        compactStreamLogs: bool = True,
        initialMsg: str = ''
    ):
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
        # Args
        self.loggerName = loggerName
        self.loggingLevel = loggingLevel
        self.allLogsFilePath = allLogsFilePath
        self.errorLogsFilePath = errorLogsFilePath
        self.timeZone = timeZone
        self.compactStreamLogs = compactStreamLogs
        
        # Variables
        self.logger = self._initiate_logger()                                                   # Logger
        self.handlers: set[logging.Handler] = set()                                             # List of all available handlers
        self.__compact_formatter = self._get_compact_formatter()
        self.__full_formatter = self._get_full_formatter()
        
        # Logging
        self._initiate_stream_logging()
        if self.allLogsFilePath:
            self._initiate_file_logging(
                self.allLogsFilePath, logging.INFO
            )
        if self.errorLogsFilePath:
            self._initiate_file_logging(
                self.errorLogsFilePath, logging.ERROR
            )
        self.raw_logging(
            initialMsg, True, True
        )

    def _initiate_logger(self):
        """ Returns `Logger` after initiating it """
        return logging.Logger(
            self.loggerName,
            self.loggingLevel
        )
    
    def _get_compact_formatter(self):
        """ Returns compact `Formatter` after initiating it for all levels """
        s1 = " " * 10
        s2 = " " * 50
        return LevelFormatter(
            {
                logging.DEBUG: f'~ %(module)s (%(lineno)d): {s1} %(message)s',
                logging.INFO: f'> %(module)s (%(lineno)d): {s1} %(message)s',
                logging.ERROR: f'[x] %(module)s (%(lineno)d): {s1} %(message)s',
            },
            timeZone=self.timeZone
        )

    def _get_full_formatter(self):
        """ Returns full `Formatter` after initiating it for all levels """
        s1 = " " * 10
        s2 = " " * 50
        return LevelFormatter(
            {
                logging.DEBUG: f'~ [%(asctime)s] [%(levelname)s: %(module)s-%(lineno)d] {s1} > %(message)s {s2} [%(threadName)s]',
                logging.INFO: f'> [%(asctime)s] [%(levelname)s: %(module)s-%(lineno)d] {s1} > %(message)s {s2} [%(threadName)s]',
                logging.ERROR: f'[x] [%(asctime)s] [%(levelname)s: %(module)s-%(lineno)d] {s1} [x] %(message)s {s2} [%(threadName)s]',
            },
            datefmt=f"%Y-%m-%d %I:%M:%S %p ({self.timeZone})",
            timeZone=self.timeZone
        )
    
    def _add_handler(self, handler: logging.Handler):
        """ Adds `handler` to `Logger` """
        self.logger.addHandler(handler)
        self.handlers.add(handler)
    
    def _initiate_stream_logging(self):
        """ Initiates logs streaming to Terminal
        - `Formatter` is based on `self.compactStreamLogs`
        """
        streamHand = logging.StreamHandler()
        streamHand.setFormatter(
            self.__compact_formatter if self.compactStreamLogs else self.__full_formatter
        )
        self._add_handler(streamHand)

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
    
    def get_logger(self):
        """ Returns `logging.Logger` object """
        return self.logger

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
        if toAllLogsFile and self.allLogsFilePath:
            write_to_file(self.allLogsFilePath)
        if toErrorLogsFile and self.errorLogsFilePath:
            write_to_file(self.errorLogsFilePath)

    def close_logging_handlers(self):
        """ Close all available handlers: All file handlers & stream handler """
        for i in self.handlers:
            i.close()
    
""" This module contains classes and methods related to logging """
import logging
from bisect import bisect
from datetime import datetime
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


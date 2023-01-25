"""
This module contains exception classes
"""




class IgnoreError(Exception):
    """ This exception should be ignored after catching it for the sake of continuity
    - You can ignore it in try-except block, or
    - By logging/printing to console
    """
    
    def __init__(self, *args: object) -> None:
        """ This exception should be ignored after catching it for the sake of continuity
        - You can ignore it in try-except block, or
        - By logging/printing to console
        """
        super().__init__(*args)

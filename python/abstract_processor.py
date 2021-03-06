"""
This file is subject to the terms and conditions defined in file 'LICENSE',
    which is part of this source code package.

Copyright 2020 Nathan Mentley
"""


from abc import ABC, abstractmethod


class AbstractProcessor(ABC):
    """
    An abstract interface to parse coverlet json output and convert it to a standard format to display.

    '''
    Methods
    -------
    get_data(file_name)
        takes a file_name and processes out the line coverage information.
    """
    @abstractmethod
    def get_data(self, file_name):
        """
        Takes a file name and processes out the line coverage data from it.
        """
        pass

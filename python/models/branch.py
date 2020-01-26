"""
This file is subject to the terms and conditions defined in file 'LICENSE',
    which is part of this source code package.

Copyright 2020 Nathan Mentley
"""


class Branch:
    """
    """
    _number = 0
    _offset = 0
    _end_offset = 0

    def __init__(self, number, offset, end_offset):
        self._number = number
        self._offset = offset
        self._end_offset = end_offset

    def set_number(self, number):
        self._number = number

    def get_number(self, number):
        return self._number

    def set_offset(self, offset):
        self._offset = offset

    def get_offset(self, offset):
        return self._offset

    def set_end_offset(self, end_offset):
        self._end_offset = end_offset

    def get_end_offset(self, end_offset):
        return self._end_offset

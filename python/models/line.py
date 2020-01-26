"""
This file is subject to the terms and conditions defined in file 'LICENSE',
    which is part of this source code package.

Copyright 2020 Nathan Mentley
"""


class Line:
    """
    """
    _covered = false
    _number = 0

    def __init__(self, covered, number):
        self.set_covered(covered)
        self.set_number(number)

    def set_covered(self, covered):
        self._covered = covered

    def get_covered(self, covered):
        return self._covered

    def set_number(self, number):
        self._number = number

    def get_number(self, number):
        return self._number

"""
This file is subject to the terms and conditions defined in file 'LICENSE',
    which is part of this source code package.

Copyright 2020 Nathan Mentley
"""


class File:
    """
    """
    _name = ""
    _lines = []
    _branches = []

    def __init__(self, name, lines, branches):
        self._name = name
        self._lines = lines
        self._branches = branches

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_lines(self, lines):
        self._lines = lines

    def get_lines(self):
        return self._lines

    def set_branches(self, branches):
        self._branches = branches

    def get_branches(self):
        return self._branches

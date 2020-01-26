from abc import ABC, abstractmethod


class AbstractReporter(ABC):
    """
    An abstract interface to display coverage data.

    '''
    Methods
    -------
    """

    @abstractmethod
    def highlight_line(self, line, fcolor, bcolor):
        """
        Highlights a line in vim using the line number, foreground color, and background color.
        """
        pass

    @abstractmethod
    def highlight_branch(self, key, branch, fcolor, bcolor):
        """
        Highlights a branch in vim using the line number + offset, foreground color, and background color.
        """
        pass

    @abstractmethod
    def clear_branch(self, key):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        pass

    @abstractmethod
    def clear_line(self, line):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        pass

    @abstractmethod
    def create_new_buffer(self, file_name, contents):
        """
        Creates a new buffer with the passed content
        """
        pass

    @abstractmethod
    def get_current_buffer_file_name(self):
        pass

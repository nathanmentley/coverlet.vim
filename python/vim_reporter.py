import vim

from abstract_reporter import AbstractReporter


class VimReporter(AbstractReporter):
    """
    An abstract interface to display coverage data.

    '''
    Methods
    -------
    """

    def _run_commands(self, commands):
        """
        runs a list of commands in vim
        """
        for command in commands:
            vim.command(command)

    def highlight_line(self, line, fcolor, bcolor):
        """
        Highlights a line in vim using the line number, foreground color, and background color.
        """
        self._run_commands([
            "highlight CoverletLine{0} ctermfg={1} ctermbg={2}".format(str(line), fcolor, bcolor),
            'let s:coverlet_match_{0} = matchaddpos("CoverletLine{1}", [[{2}, 1, 1]])'.format(str(line), str(line), str(line))
        ])

    def highlight_branch(self, key, branch, fcolor, bcolor):
        """
        Highlights a branch in vim using the line number + offset, foreground color, and background color.
        """
        self._run_commands([
            "highlight CoverletBranch{0} ctermfg={1} ctermbg={2}".format(key, fcolor, bcolor),
            'let s:coverlet_branch_match_{0} = matchaddpos("CoverletBranch{1}", [[{2}, {3}, {4}]])'.format(key, key, branch["line"], branch["offset"], branch["endOffset"])
        ])

    def clear_branch(self, key):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        vim.eval('matchdelete(s:coverlet_branch_match_{0})'.format(key))

    def clear_line(self, line):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        vim.eval('matchdelete(s:coverlet_match_{0})'.format(str(line)))

    def create_new_buffer(self, file_name, contents):
        """
        Creates a new buffer with the passed content
        """
        self._run_commands([
            'rightbelow vsplit {0}'.format(file_name),
            'normal! ggdG',
            'setlocal buftype=nowrite',
            'call append(0, {0})'.format(contents)
        ])

    def get_current_buffer_file_name(self):
        return vim.current.buffer.name

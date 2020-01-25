import json
import time
import vim

class Coverlet:
    """
    A class to parse coverlet json output, and display the results in vim.

    '''
    Attributes
    ----------

    _coverlet_data : dictionary
        *private* A collection of file names to line coverage information.

    _foreground_color: str
        *private* The currently configured foreground color for highlighted lines.

    _uncovered_line_color: str
        *private* The currently configured background color for uncovred lines.

    _covered_line_color: str
        *private* The currently configured background color for covered lines.

    _coverlet_file: str
        *private* The currently configured file path to the coverlet json file.

    Methods
    =======
    clear_highlights()
        Clears the highlighting created in vim to display the coverlet data.

    refresh_coverlet()
        Reloads the coverlet data from the json source and displays highlights in vim to visually show the data.
    """

    _coverlet_data = {}

    _highlighted_lines = []

    # TODO: Make these values configurable from vimrc or project specific config
    _foreground_color = "black"
    _uncovered_line_color = "red"
    _covered_line_color = "green"
    _coverlet_file = "/Users/nathanmentley/Projects/coverlet_tests/coverage.json"

    def __init__(self):
        """
        Ctor. Thi will load the coverlet data if it's found.
        """
        self._load_coverlet_content()

    def _process_method(self, file_key, method_key, method_value):
        """
        Processes the method node from the coverlet json, and populates those values in the _coverlet_data attribute.
        """
        for line_key, line_value in method_value["Lines"].items():
            if line_value == 0:
                self._coverlet_data['files'][file_key]['uncovered_lines'].append(int(line_key))
            else:
                self._coverlet_data['files'][file_key]['covered_lines'].append(int(line_key))

    def _load_coverlet_content(self):
        """
        Reloads the coverlet data from the json source and displays highlights in vim to visually show the data.
        """
        self.clear_highlights()
        self._coverlet_data['files'] = {}

        with open(self._coverlet_file) as json_file:
            data = json.load(json_file)
            for module_key, module_value in data.items():
                for file_key, file_value in module_value.items():
                    self._coverlet_data['files'][file_key] = {}
                    self._coverlet_data['files'][file_key]['covered_lines'] = []
                    self._coverlet_data['files'][file_key]['uncovered_lines'] = []

                    for class_key, class_value in file_value.items():
                        for method_key, method_value in class_value.items():
                            self._process_method(file_key, method_key, method_value)

        self._highlight_lines()

    def _highlight_line(self, line, fcolor, bcolor):
        """
        Highlights a line in vim using the line number, foreground color, and background color.
        """
        if not line in self._highlighted_lines:
            self._highlighted_lines.append(line)
        vim.command("highlight CoverletLine" + str(line) + " ctermfg=" + fcolor + " ctermbg=" + bcolor)
        vim.command('let s:coverlet_match_' + str(line) + ' = matchaddpos("CoverletLine' + str(line) + '", [0, ' + str(line) + '])')

    def _clear_line(self, line):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        vim.eval('matchdelete(s:coverlet_match_' + str(line) + ')')

    def _get_uncovered_lines(self, file_name):
        """
        Pulls a list of uncovered line numbers from our processed coverlet data.
        """
        if file_name in self._coverlet_data['files'].keys():
            return self._coverlet_data['files'][file_name]['uncovered_lines']
        else:
            return []

    def _get_covered_lines(self, file_name):
        """
        Pulls a list of covered line numbers from our processed coverlet data.
        """
        if file_name in self._coverlet_data['files'].keys():
            return self._coverlet_data['files'][file_name]['covered_lines']
        else:
            return []

    def _highlight_lines(self):
        """
        For the current buffer. We get the full file name and try to markup the file with coverage data.
        """
        current_buff = vim.current.buffer
        print(current_buff.name)

        for line in self._get_uncovered_lines(current_buff.name):
            self._highlight_line(line, self._foreground_color, self._uncovered_line_color)
        for line in self._get_covered_lines(current_buff.name):
            self._highlight_line(line, self._foreground_color, self._covered_line_color)

    def clear_highlights(self):
        """
        Clears the highlighting created in vim to display the coverlet data.
        """
        for line in self._highlighted_lines:
            self._clear_line(line)
        self._highlighted_lines = []

    def refresh_coverlet(self):
        """
        Reloads the coverlet data from the json source and displays highlights in vim to visually show the data.
        """
        self._load_coverlet_content()

import json
import os
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

    _branch_color: str
        *private* The currently configured background color for uncovered branches.

    _coverlet_file: str
        *private* The currently configured file path to the coverlet json file.

    Methods
    -------

    display_coverage_info_buffer()
        Displays a list of uncovered lines, and branches in a new buffer and pane.

    clear_highlights()
        Clears the highlighting created in vim to display the coverlet data.

    refresh_coverlet()
        Reloads the coverlet data from the json source and displays highlights in vim to visually show the data.
    """

    _coverlet_data = {}

    _highlighted_lines = []
    _highlighted_branches = []

    _coverlet_file = ""
    _foreground_color = ""
    _uncovered_line_color = ""
    _covered_line_color = ""
    _branch_color = ""

    def __init__(self, file_name, fg_color = "black", uncovered_color = "red", covered_color = "green", branch_color = "yellow"):
        """
        Ctor. Sets private values from vim configuration.
        """
        self._coverlet_file = file_name
        self._foreground_color = fg_color
        self._uncovered_line_color = uncovered_color
        self._covered_line_color = covered_color
        self._branch_color = branch_color

    def _run_commands(self, commands):
        """
        runs a list of commands in vim
        """
        for command in commands:
            vim.command(command)

    def _process_method(self, file_key, method_key, method_value):
        """
        Processes the method node from the coverlet json, and populates those values in the _coverlet_data attribute.
        """
        for line_key, line_value in method_value["Lines"].items():
            # If the line value is 0 no test run has hit this line. Lets mark it as uncovered.
            if line_value == 0:
                self._coverlet_data['files'][file_key]['uncovered_lines'].append(int(line_key))
            else:
                self._coverlet_data['files'][file_key]['covered_lines'].append(int(line_key))
        for branch in  method_value["Branches"]:
            if branch["Hits"] == 0:
                self._coverlet_data['files'][file_key]['branches'].append({
                    "line": branch["Line"],
                    "offset": branch["Offset"],
                    "endOffset": branch["EndOffset"],
                    "path": branch["Path"],
                    "ordinal": branch["Ordinal"]
                })


    def _load_coverlet_content(self):
        """
        Reloads the coverlet data from the json source and displays highlights in vim to visually show the data.
        """
        self._coverlet_data['files'] = {}

        if not os.path.exists(self._coverlet_file):
            print("Could not load coverlet file: " + self._coverlet_file)
            return

        with open(self._coverlet_file) as json_file:
            data = json.load(json_file)
            for module_key, module_value in data.items():
                for file_key, file_value in module_value.items():
                    self._coverlet_data['files'][file_key] = {}

                    self._coverlet_data['files'][file_key]['covered_lines'] = []
                    self._coverlet_data['files'][file_key]['uncovered_lines'] = []
                    self._coverlet_data['files'][file_key]['branches'] = []

                    for class_key, class_value in file_value.items():
                        for method_key, method_value in class_value.items():
                            self._process_method(file_key, method_key, method_value)

    def _highlight_line(self, line, fcolor, bcolor):
        """
        Highlights a line in vim using the line number, foreground color, and background color.
        """
        if not line in self._highlighted_lines:
            self._highlighted_lines.append(line)
        self._run_commands([
            "highlight CoverletLine{0} ctermfg={1} ctermbg={2}".format(str(line), fcolor, bcolor),
            'let s:coverlet_match_{0} = matchaddpos("CoverletLine{1}", [{2}])'.format(str(line), str(line), str(line))
        ])

    def _highlight_branch(self, branch, fcolor, bcolor):
        """
        Highlights a branch in vim using the line number + offset, foreground color, and background color.
        """
        key = "{0}_{1}_{2}".format(branch["line"], branch["offset"], branch["endOffset"])
        if not key in self._highlighted_branches:
            self._highlighted_branches.append(key)
        self._run_commands([
            "highlight CoverletBranch{0} ctermfg={1} ctermbg={2}".format(key, fcolor, bcolor),
            'let s:coverlet_branch_match_{0} = matchaddpos("CoverletBranch{1}", [{2}])'.format(key, key, branch["line"])
        ])

    def _clear_branch(self, key):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        vim.eval('matchdelete(s:coverlet_branch_match_{0})'.format(key))

    def _clear_line(self, line):
        """
        Removes a coverlet highlight in vim. This won't affect highlighting markup from other plugins.
        """
        vim.eval('matchdelete(s:coverlet_match_{0})'.format(str(line)))

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

    def _get_branches(self, file_name):
        """
        Pulls a list of branch coverage.
        """
        if file_name in self._coverlet_data['files'].keys():
            return self._coverlet_data['files'][file_name]['branches']
        else:
            return []

    def _highlight_lines(self):
        """
        For the current buffer. We get the full file name and try to markup the file with coverage data.
        """
        current_buff = vim.current.buffer

        for line in self._get_uncovered_lines(current_buff.name):
            self._highlight_line(line, self._foreground_color, self._uncovered_line_color)

        for line in self._get_covered_lines(current_buff.name):
            self._highlight_line(line, self._foreground_color, self._covered_line_color)

        for branch in self._get_branches(current_buff.name):
            self._highlight_branch(branch, self._foreground_color, self._branch_color)

    def _create_new_buffer(self, file_name, contents):
        """
        Creates a new buffer with the passed content
        """
        self._run_commands([
            'rightbelow vsplit {0}'.format(file_name),
            'normal! ggdG',
            'setlocal buftype=nowrite',
            'call append(0, {0})'.format(contents)
        ])

    def display_coverage_info_buffer(self):
        data = ["Coverage Data"]

        for file_name in self._coverlet_data['files']:
            for line in self._coverlet_data['files'][file_name]['uncovered_lines']:
                data.append("{0}:{1} not covered.".format(file_name, line))
            for branch in self._coverlet_data['files'][file_name]['branches']:
                data.append("{0}:{1} branch uncovered.".format(file_name, branch["line"]))

        self._create_new_buffer("Coverage Info", data)

    def clear_highlights(self):
        """
        Clears the highlighting created in vim to display the coverlet data.
        """
        for line in self._highlighted_lines:
            self._clear_line(line)
        self._highlighted_lines = []
        for key in self._highlighted_branches:
            self._clear_branch(key)
        self._highlighted_branches = []

    def refresh_coverlet(self):
        """
        Reloads the coverlet data from the json source and displays highlights in vim to visually show the data.
        """
        self.clear_highlights()
        self._load_coverlet_content()
        self._highlight_lines()

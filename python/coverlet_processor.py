import json
import os

from abstract_processor import AbstractProcessor


class CoverletProcessor(AbstractProcessor):
    """
    A class to parse coverlet json output and convert it to a standard format to display.

    '''
    Methods
    -------
    get_data(file_name)
        takes a file_name and processes out the line coverage information.
    """
    def _process_method(self, ret, file_key, method_key, method_value):
        """
        Processes the method node from the coverlet json, and populates those values in the _coverlet_data attribute.
        """
        for line_key, line_value in method_value["Lines"].items():
            # If the line value is 0 no test run has hit this line. Lets mark it as uncovered.
            if line_value == 0:
                ret[file_key]['uncovered_lines'].append(int(line_key))
            else:
            # else let's mark it as covered.
                ret[file_key]['covered_lines'].append(int(line_key))
        for branch in  method_value["Branches"]:
            # Only import branch info if the branch path isn't taken.
            if branch["Hits"] == 0:
                branch_data = {
                    "line": branch["Line"],
                    "offset": branch["Offset"],
                    "endOffset": branch["EndOffset"],
                    "path": branch["Path"],
                    "ordinal": branch["Ordinal"]
                }
                ret[file_key]['branches'].append(branch_data)

    def get_data(self, file_name):
        """
        Takes a file name and processes out the line coverage data from it.
        """
        ret = {}

        if not os.path.exists(file_name):
            # exit without issue if the file cannot be found.
            print("Could not load coverlet file: " + file_name)
            return

        with open(file_name) as json_file:
            data = json.load(json_file)
            # for each module
            for module_key, module_value in data.items():
                # for each file
                for file_key, file_value in module_value.items():
                    # setup a new file node in the data structure
                    ret[file_key] = {}

                    ret[file_key]['covered_lines'] = []
                    ret[file_key]['uncovered_lines'] = []
                    ret[file_key]['branches'] = []

                    for class_key, class_value in file_value.items():
                        for method_key, method_value in class_value.items():
                            # for each method in each class
                            self._process_method(ret, file_key, method_key, method_value)
        return ret

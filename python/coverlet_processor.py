from abc import ABC, abstractmethod
import json
import os
import vim


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
                ret[file_key]['covered_lines'].append(int(line_key))
        for branch in  method_value["Branches"]:
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
            print("Could not load coverlet file: " + file_name)
            return

        with open(file_name) as json_file:
            data = json.load(json_file)
            for module_key, module_value in data.items():
                for file_key, file_value in module_value.items():
                    ret[file_key] = {}

                    ret[file_key]['covered_lines'] = []
                    ret[file_key]['uncovered_lines'] = []
                    ret[file_key]['branches'] = []

                    for class_key, class_value in file_value.items():
                        for method_key, method_value in class_value.items():
                            self._process_method(ret, file_key, method_key, method_value)
        return ret

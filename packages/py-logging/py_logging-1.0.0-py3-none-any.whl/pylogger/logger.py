from pylogger.formatters.level import get_log_level_formatter
from pylogger.formatters.scope import get_scope
from pylogger.formatters.list import format_list
from pylogger.formatters.dictionary import format_dict


class Logger:
    def __init__(self):
        self.scope = False

    def set_options(self, value: dict):
        if "scope" in value.keys():
            self.scope = value.get("scope")

    def log(self, level, content):
        final_string = ""
        if self.scope:
            final_string += get_scope()
        final_string += get_log_level_formatter(level)
        if type(content) is list:
            print(final_string + "List:")
            format_list(content)
        elif type(content) is dict:
            print(final_string + "Dictionary:")
            format_dict(content)
        else:
            print(final_string + str(content))
            return

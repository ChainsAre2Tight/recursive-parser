from dataclasses import dataclass
from internals.handlers import eventhandler

from internals.exceptions import UnknownBrowserError, ConfigNotFoundError
from internals.file_utils import construct_file_name_from_link, validate_file_name


@dataclass
class Config:
    start_page: str  # Where to start scraping
    maximum_recursion_depth: int  # Maximum recursion dept when performing recursion search
    browser: str  # Chrome or Firefox
    wait_time: int  # how much time to give each page to load
    printout: bool  # if eventhandler should print everything
    mode: str  # strict or normal
    graph_file_name: str
    pickle_dump_file_name: str
    cookies: bool
    log: bool
    get_directories: bool
    strip_GET_params: bool


class ConfigParser:

    @staticmethod
    def parse():
        from app.config import config as my_config
        try:
            eventhandler.new_status("Loading config...")

            # Check if import is successful
            try:
                len(my_config.start_page)
                eventhandler.new_event("Found configuration object")
            except ImportError as err:
                eventhandler.new_error("Couldn't find configuration object")
                raise err

            # Here be config validations
            if my_config.maximum_recursion_depth < 0:
                raise ValueError("Recursion depth should be non-negative")
            eventhandler.new_event("Recursion depth is valid")
            if my_config.browser not in ['Firefox', 'Chrome']:
                raise UnknownBrowserError('Browser should be either Chrome or Firefox')
            eventhandler.new_event("Browser is valid")
            if my_config.wait_time < 0:
                raise ValueError("Wait time must be non-negative")
            elif my_config.wait_time > 60:
                eventhandler.new_event("Wait time should be lower than 60")
            eventhandler.new_event("Wait time is valid")

            if type(my_config.printout) != bool:
                raise TypeError("Printout should be either True or False")

            if type(my_config.log) != bool:
                raise TypeError("Logging should be either True or False")

            if my_config.mode not in ['normal', 'semi-strict', 'strict']:
                raise ValueError(f'Expected "normal", "semi-strict" or "strict", got: {my_config.mode}')

            if type(my_config.cookies) != bool:
                raise TypeError("Cookies should be either True or False")

            if my_config.pickle_dump_file_name == 'auto':
                my_config.pickle_dump_file_name = construct_file_name_from_link(
                    my_config.start_page,
                    f'dump-{my_config.mode}',
                    f'l{my_config.maximum_recursion_depth}'
                )
                eventhandler.new_info(f'Dump file name set to Auto. New file name: "{my_config.pickle_dump_file_name}"')

            if not validate_file_name(my_config.pickle_dump_file_name):
                raise ValueError("Dump file name shouldn't contain any of the special characters, not even file format")

            if my_config.graph_file_name == 'auto':
                my_config.graph_file_name = construct_file_name_from_link(
                    my_config.start_page,
                    f'graph-{my_config.mode}',
                    f'l{my_config.maximum_recursion_depth}{"-merged" if my_config.strip_GET_params else ""}'
                )
                eventhandler.new_info(f'Graph file name set to Auto. New file name: "{my_config.graph_file_name}"')

            if not validate_file_name(my_config.graph_file_name):
                raise ValueError("Graph file name shouldn't contain any of the special characters, not even file format")

            if type(my_config.get_directories) != bool:
                raise TypeError("get_directories should be either True or False")

            if type(my_config.strip_GET_params) != bool:
                raise TypeError("strip_GET_params should be either True or False")

            # return config object
            eventhandler.new_status("Successfully loaded config")
            if not my_config.printout:
                eventhandler.new_info("Printing is disabled")
                eventhandler.printout = False
            if not my_config.log:
                eventhandler.new_info("Logging is disabled. Config ends here")
                eventhandler.write = False

            return my_config
        except ImportError:
            raise ConfigNotFoundError("Missing config definition for app/config.py")
        except ValueError as err:
            raise err


if __name__ == "__main__":
    print(ConfigParser.parse())

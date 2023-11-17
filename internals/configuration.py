from dataclasses import dataclass

from internals.exceptions import UnknownBrowserError, ConfigNotFoundError


@dataclass
class Config:
    start_page: str  # Where to start scraping
    maximum_recursion_depth: int  # Maximum recursion dept when performing recursion search
    browser: str  # Chrome or Firefox


class ConfigParser:

    @staticmethod
    def parse():
        from app.config import config as my_config
        try:

            # Check if import is successful
            try:
                len(my_config.start_page)
            except ImportError as err:
                raise err

            # Here be config validations
            if my_config.maximum_recursion_depth < 0:
                raise ValueError("Recursion depth should be non-negative")
            if my_config.browser not in ['Firefox', 'Chrome']:
                raise UnknownBrowserError('Browser should be either Chrome or Firefox')

            # return config object
            return my_config
        except ImportError:
            raise ConfigNotFoundError("Missing config definition for app/config.py")
        except ValueError as err:
            raise err


if __name__ == "__main__":
    print(ConfigParser.parse())

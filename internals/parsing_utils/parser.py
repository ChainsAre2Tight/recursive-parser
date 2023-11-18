from bs4 import BeautifulSoup

from selenium import webdriver
import selenium.common.exceptions

from internals.exceptions import UnknownRequestTypeError, UnknownBrowserError, PageCouldntBeReachedError
from internals.handlers import eventhandler
import time
from internals.timeout import timeout, MyTimeout


class Parser:

    def __init__(self, browser: str, wait_time: int):
        eventhandler.new_status("Initiating browser...")
        start_time = time.time()

        def set_options(options_obj):
            pass
            options_obj.add_argument('--headless')
            # options_obj.add_argument('window-size=1920x1080')
            # options_obj.add_argument("disable-gpu")

        if browser == 'Firefox':
            eventhandler.new_status("Loading Firefox...")
            from selenium.webdriver.firefox.options import Options
            options = Options()
            set_options(options)
            self.driver = webdriver.Firefox(options=options)
        elif browser == 'Chrome':
            eventhandler.new_status("Loading Chrome...")
            from selenium.webdriver.chrome.options import Options
            options = Options()
            set_options(options)
            self.driver = webdriver.Chrome(options=options)
        else:
            eventhandler.new_error("Couldn't load specified browser")
            raise UnknownBrowserError

        eventhandler.new_status(f"Browser successfully initiated in {round(time.time() - start_time, 3)} seconds")
        self.driver.implicitly_wait(wait_time)

    def __del__(self):
        self.driver.close()

    @timeout(30)
    def parse_page(self, link: str, method="GET", sleep_time: int = 0) -> tuple[BeautifulSoup, list[dict]]:
        if sleep_time > 0:
            eventhandler.new_status(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            eventhandler.new_status(f'Slept for {sleep_time} seconds, now back to parsing')
        start_time = time.time()
        if method == "GET":
            eventhandler.new_status(f'Trying to GET page at {link}  ...')
            try:
                self.driver.get(link)
            except selenium.common.exceptions.WebDriverException as er:
                eventhandler.new_error(f"Couldn't reach page at {link}. Skipping.")
                raise PageCouldntBeReachedError(er.args)

        elif method == "POST":
            eventhandler.new_status(f'Trying to POST page at {link} ...')
            # TODO handle post data
            raise NotImplementedError
        else:
            raise UnknownRequestTypeError("Request method should be either GET or POST")

        eventhandler.new_status(f'Page successfully loaded in {round(time.time() - start_time, 3)} seconds')

        # get soup
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # get cookies
        cookies = self.driver.get_cookies()
        eventhandler.new_status("Successfully got soup and cookies of this page")
        return soup, cookies


if __name__ == "__main__":
    pass

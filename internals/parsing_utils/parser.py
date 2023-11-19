from bs4 import BeautifulSoup

from selenium import webdriver
import selenium.common.exceptions

from internals.exceptions import UnknownRequestTypeError, UnknownBrowserError, PageCouldntBeReachedError
from internals.handlers import eventhandler
import time
from internals.timeout import timeout, MyTimeout
from internals.objects import Page

from internals.parsing_utils.utils import same_domain, same_website
from internals.parsing_utils.scrapper import Scrapper

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

    def recursive_parse(self, link, ttl: int, parsed_pages: dict[Page], sleep_time: int,
                        known_links: dict[str], mode: str):
        if ttl > 0:
            try:
                try:
                    soup, cookies = self.parse_page(link, method="GET", sleep_time=sleep_time)
                    print(cookies)
                except TypeError:
                    raise PageCouldntBeReachedError
                page = Scrapper.scrap(soup, link, cookies, known_links)
                parsed_pages[link] = page

                for sub_page in page.links:
                    if mode == 'strict' and not same_website(link, sub_page):
                        continue
                    elif mode == 'semi-strict' and not same_domain(link, sub_page):
                        continue
                    elif mode == 'normal':
                        pass

                    if sub_page not in parsed_pages.keys():
                        self.recursive_parse(
                            link=sub_page,
                            ttl=ttl - 1,
                            parsed_pages=parsed_pages,
                            sleep_time=sleep_time,
                            known_links=known_links,
                            mode=mode,
                        )
            except MyTimeout:
                eventhandler.new_error(f"Timeout when trying to parse {link}. Skipping")
                parsed_pages[link] = link
            except PageCouldntBeReachedError:
                eventhandler.new_error(f"Couldn't reach {link}. Skipping")
                parsed_pages[link] = link


if __name__ == "__main__":
    pass

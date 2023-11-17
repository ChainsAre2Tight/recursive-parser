from bs4 import BeautifulSoup

from selenium import webdriver

from internals.exceptions import UnknownRequestTypeError, UnknownBrowserError


class Parser:

    def __init__(self, browser: str, wait_time: int):
        def set_options(options_obj):
            options_obj.add_argument('--headless')
            # options_obj.add_argument('window-size=1920x1080')
            # options_obj.add_argument("disable-gpu")

        if browser == 'Firefox':
            from selenium.webdriver.firefox.options import Options
            options = Options()
            set_options(options)
            self.driver = webdriver.Firefox(options=options)
        elif browser == 'Chrome':
            from selenium.webdriver.chrome.options import Options
            options = Options()
            set_options(options)
            self.driver = webdriver.Chrome(options=options)
        else:
            raise UnknownBrowserError

        self.driver.implicitly_wait(wait_time)

    def __del__(self):
        self.driver.close()

    def parse_page(self, link: str, method="GET") -> tuple[BeautifulSoup, list[dict]]:
        if method == "GET":
            self.driver.get(link)
        elif method == "POST":
            # TODO handle post data
            raise NotImplementedError
        else:
            raise UnknownRequestTypeError("Request method should be either GET or POST")

        # get soup
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # get cookies
        cookies = self.driver.get_cookies()

        return soup, cookies


if __name__ == "__main__":
    pass

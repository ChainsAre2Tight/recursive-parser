from internals.parsing_utils.parser import Parser
from internals.parsing_utils.scrapper import Scrapper
from internals.configuration import ConfigParser


def main():
    config = ConfigParser.parse()
    link = config.start_page
    browser = config.browser

    soup, cookies = Parser(browser=browser, wait_time=10).parse_page(link, method="GET")
    page = Scrapper.scrap(soup, link, cookies)

    print(page)


if __name__ == "__main__":
    main()

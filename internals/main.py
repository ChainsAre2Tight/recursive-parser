from internals.parser import Parser
from internals.scrapper import Scrapper
from internals.configuration import ConfigParser
import requests


def main():
    config = ConfigParser.parse()
    link = config.start_page

    session = requests.session()
    soup, cookies = Parser.parse_page(link, method="GET", session=session)
    page = Scrapper.scrap(soup, link, cookies)

    print(page)
    print(cookies)


if __name__ == "__main__":
    main()

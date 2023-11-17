from internals.parser import Parser
from internals.scrapper import Scrapper
from internals.configuration import ConfigParser


def main():
    config = ConfigParser.parse()
    link = config.start_page
    soup = Parser.parse_page(link)
    page = Scrapper.scrap(soup)

    print(page)


if __name__ == "__main__":
    main()

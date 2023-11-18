import time

from internals.parsing_utils.parser import Parser
from internals.parsing_utils.scrapper import Scrapper
from internals.configuration import ConfigParser
from internals.handlers import eventhandler
from internals.exceptions import PageCouldntBeReachedError
from internals.objects import Page
from internals.visualisation.graph_builder import GraphBuilder
import networkx as nx
import pyvis.network

from internals.timeout import MyTimeout


def main_0():
    try:
        config = ConfigParser.parse()
        link = config.start_page
        browser = config.browser

        soup, cookies = Parser(browser=browser, wait_time=10).parse_page(link, method="GET")
        page = Scrapper.scrap(soup, link, cookies)

        print(page)
    except PageCouldntBeReachedError as er:
        pass
    finally:
        print("Events: ", *eventhandler.events, sep='\n    ')


def recursive_parse(link, ttl: int, parser: Parser, parsed_pages: dict[Page], sleep_time: int,
                    known_links: dict[str]):
    if ttl > 0:
        try:
            try:
                soup, cookies = parser.parse_page(link, method="GET", sleep_time=sleep_time)
            except TypeError:
                raise PageCouldntBeReachedError
            page = Scrapper.scrap(soup, link, cookies, known_links)
            parsed_pages[link] = page

            for sub_page in page.links:
                if sub_page not in parsed_pages.keys():
                    recursive_parse(
                        link=sub_page,
                        ttl=ttl - 1,
                        parser=parser,
                        parsed_pages=parsed_pages,
                        sleep_time=sleep_time,
                        known_links=known_links,
                    )
        except MyTimeout:
            eventhandler.new_error(f"Timeout when trying to parse {link}. Skipping")
            parsed_pages[link] = link
        except PageCouldntBeReachedError:
            eventhandler.new_error(f"Couldn't reach {link}. Skipping")
            parsed_pages[link] = link


def main():
    start_time = time.time()

    config = ConfigParser.parse()
    link = config.start_page
    browser = config.browser
    parser = Parser(
        browser=browser,
        wait_time=config.wait_time,
    )

    parsed_pages: dict[Page | str] = dict()
    known_links = dict()

    if 1:
        pass
    try:

        recursive_parse(
            link=link,
            ttl=config.maximum_recursion_depth,
            parser=parser,
            parsed_pages=parsed_pages,
            sleep_time=5,
            known_links=known_links,
        )
        eventhandler.new_info('All clear')
    except Exception as er:
        raise er
    finally:
        eventhandler.new_info(f"Finished in {round(time.time() - start_time, 3)} seconds")
        # print("Events: ", *eventhandler.events, sep='\n    ')
        graph, nodes = GraphBuilder.graph_from_parsed_pages(parsed_pages)
        GraphBuilder.export_graph(graph, nodes, "result.html")



if __name__ == "__main__":
    main()

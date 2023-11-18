import time

from internals.parsing_utils.parser import Parser
from internals.handlers import eventhandler
from internals.objects import Page
from internals.visualisation.graph_builder import GraphBuilder
import pickle


def perform_parsing(config):
    eventhandler.new_status("Starting parsing routine...")
    start_time = time.time()

    link = config.start_page
    browser = config.browser
    parser = Parser(
        browser=browser,
        wait_time=config.wait_time,
    )

    parsed_pages: dict[Page | str] = dict()
    known_links = dict()
    exit_code = "Unhandled error"
    try:
        try:
            parser.recursive_parse(
                link=link,
                ttl=config.maximum_recursion_depth,
                parsed_pages=parsed_pages,
                sleep_time=1,
                known_links=known_links,
                mode='strict',
            )
            eventhandler.new_info('All clear')
            exit_code = 'Normal'
        except Exception as er:
            exit_code = f'Error: {er}'
            raise er
        finally:
            eventhandler.new_info(f"Finished in {round(time.time() - start_time, 3)} seconds")

            eventhandler.new_status(f"Dumping parsed data to {config.pickle_dump_file_name}...")
            with open(config.pickle_dump_file_name, 'wb') as f:
                pickle.dump(parsed_pages, f, pickle.HIGHEST_PROTOCOL)
                eventhandler.new_status(f'Dump successful')
                del parsed_pages
    except KeyboardInterrupt:
        exit_code = 'KeyboardInterrupt'
    finally:
        eventhandler.new_status(f'Parsing routine completed with exit code {exit_code}')
        del eventhandler


def construct_graph(config):
    eventhandler.new_status('Starting graph constructing routine...')
    exit_code = "Unhandled error"

    try:
        eventhandler.new_status(f"Trying to read data from {config.pickle_dump_file_name}...")
        with open(config.pickle_dump_file_name, 'rb') as f:
            parsed_pages = pickle.load(f)

        eventhandler.new_status(f"Successfully read dump, {len(parsed_pages.keys())} pages loaded")

        eventhandler.new_status(f'Building graph...')
        graph, nodes = GraphBuilder.graph_from_parsed_pages(parsed_pages)
        eventhandler.new_status("Graph successfully built")

        eventhandler.new_status(f'Exporting graph to {config.graph_file_name}...')
        GraphBuilder.export_graph(graph, nodes, config.graph_file_name)
        eventhandler.new_status(f'Graph exported. All clear')
        exit_code = 'Normal'
    except KeyboardInterrupt:
        exit_code = 'KeyboardInterrupt'
    except Exception as er:
        exit_code = f"Error: {er}"
    finally:
        eventhandler.new_status(f'Graph construction routine completed with exit code {exit_code}')


if __name__ == "__main__":
    # perform_parsing()
    # construct_graph()
    pass

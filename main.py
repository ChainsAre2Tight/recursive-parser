from internals.configuration import ConfigParser
from internals.routines import perform_parsing_routine, construct_graph_routine
from internals.handlers import eventhandler
import sys

sys.setrecursionlimit(1000)


def main():
    config = ConfigParser.parse()

    try:
        task = sys.argv[1]
    except IndexError:
        task = input("? What task to perform? parse/export\n< ")

    if task == 'parse':
        perform_parsing_routine(config)
    elif task == 'export':
        construct_graph_routine(config)
    elif task == 'both':
        perform_parsing_routine(config)
        construct_graph_routine(config)
    else:
        print('Unknown task. Leaving.')

    eventhandler.__del__()


if __name__ == '__main__':
    main()

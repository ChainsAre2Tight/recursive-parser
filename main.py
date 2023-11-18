from internals.configuration import ConfigParser
from internals.main import perform_parsing, construct_graph


def main():
    config = ConfigParser.parse()

    task = input("? What task to perform? parse/export\n< ")
    if task == 'parse':
        perform_parsing(config)
    elif task == 'export':
        construct_graph(config)
    else:
        print('Unknown task. Leaving.')


if __name__ == '__main__':
    main()

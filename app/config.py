from internals.configuration import Config

config = Config(
    start_page="https://palchevsky.ru/",
    # what page should be scanned
    maximum_recursion_depth=3,
    # Maximum depth the parser is allowed (e.g. l1 will scan only the first page, l2 all the links found in l1 scan
    browser='Firefox',
    # Browser (Chrome or Firefox)
    wait_time=15,
    # How long till browser assumes page is fully loaded
    printout=True,
    # Whether to print all events into console
    log=True,
    # Whether to log all events to logging file
    pickle_dump_file_name='auto',
    graph_file_name='auto',
    # File names that will be used to store data. Set to 'auto' for automatic generation based on start_page
    mode='semi-strict',
    # normal - scan all links regardless of where they might lead
    # semi-strict - scan all links on the same website e.g. uk.example.com is considered the same website as example.com
    # strict - only the exact domain will be scanned
    cookies=False,
    # If set to False, parser will still try to access cookies but graphs built in this mode will not include them
    # set this to False for scans all scans whose depth exceed 2 as the graph will be bloated with cookie data
    get_directories=True,
    # If set to True, graph will also group scanned pages by their directory on the websites
    strip_GET_params=True,
)

from internals.configuration import Config

config = Config(
    start_page="https://example.com",
    # start_page='https://codeby.games/categories/web/cdd2d7e7-495e-4a14-b0ea-cae75b7b21a3',
    # start_page='http://62.173.140.174:16000/',
    # start_page='https://www.wolframalpha.com/',
    # start_page='https://palchevsky.ru/',
    # start_page='https://palchevsky.ru/awards.php',
    # start_page='https://palchevsky.ru/r.php?r=https://www.elibrary.ru/item.asp?id=38251321',
    # start_page='https://gettransfer.com/ru',
    # start_page='http://www.fa.ru/Pages/Home.aspx',
    maximum_recursion_depth=1,
    browser='Firefox',
    wait_time=15,
    printout=True,
    pickle_dump_file_name='./data/pickle_test',
    graph_file_name='result_test.html',
    mode='strict',
)

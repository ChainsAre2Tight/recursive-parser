import requests
from bs4 import BeautifulSoup


class UnknownRequestTypeError(Exception):
    pass


class Parser:

    @staticmethod
    def parse_page(link: str, method="GET", data=None, session: requests.session = None) -> tuple[BeautifulSoup, dict]:
        # Here be used Requests
        if session is not None:
            target = session
        else:
            target = requests
        if method == "GET":
            response = target.get(link)
        elif method == "POST":
            # TODO handle post data
            raise NotImplementedError
        else:
            raise UnknownRequestTypeError("Request method should be either GET or POST")

        # get soup
        soup = BeautifulSoup(response.content, "html.parser")

        # get cookies
        cookies = response.cookies.get_dict()
        print(response.cookies)

        return soup, cookies


if __name__ == "__main__":
    html = Parser.parse_page("https://example.com")
    print(html)

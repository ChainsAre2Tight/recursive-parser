from objects import Page, Form, Field, Cookie
from bs4 import BeautifulSoup


class Scrapper:
    @staticmethod
    def scrap(soup: BeautifulSoup, address: str, cookies: dict) -> Page:
        # get title
        title = soup.find("title").string

        # get links
        links = list(map(lambda x: x['href'], soup.find_all(href=True)))

        # get forms
        forms = list()

        # get cookies
        cookies_list = list()
        for key, value in cookies.items():
            cookies_list.append(Cookie(
                name=key,
                value=value,
            ))

        # construct Page object
        page = Page(
            address=address,
            title=title,
            links=links,
            forms=forms,
            cookies=cookies_list,
        )

        # return it
        return page

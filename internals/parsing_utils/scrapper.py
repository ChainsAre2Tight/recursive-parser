import urllib3

from internals.objects import Page, Form, Field, Cookie, CookieSource, ReferencedObject
from bs4 import BeautifulSoup

import requests


def get_content_type(url):
    response = requests.head(url)
    return response.headers['Content-Type']


class Scrapper:
    @staticmethod
    def scrap(soup: BeautifulSoup, address: str, cookies: dict) -> Page:
        # get title
        title = soup.find("title").string

        # get links
        all_links = list(map(lambda x: x['href'], soup.find_all(href=True)))
        links = list()
        objects = list()
        for item in all_links:
            link = item
            if item[:4] != 'http' and item[0] == '/':
                link = address + item[1:]

            if link.count('/') >= 3 and link.rfind('.') > link.rfind('/'):
                guessed_type = get_content_type(link)

                if 'text/html' in guessed_type:
                    links.append(link)
                else:
                    objects.append(ReferencedObject(
                        link=link,
                        object_type=guessed_type,
                    ))
            else:
                links.append(link)

        # get forms
        forms = list()

        # get cookies
        cookie_sources = list()
        for source in cookies:
            cookies_list = list()
            for key, value in source.items():
                cookies_list.append(Cookie(key, value))
            cookie_sources.append(CookieSource(cookies_list))

        # construct Page object
        page = Page(
            address=address,
            title=title,
            links=links,
            objects=objects,
            forms=forms,
            cookies=cookie_sources,
        )

        # return it
        return page

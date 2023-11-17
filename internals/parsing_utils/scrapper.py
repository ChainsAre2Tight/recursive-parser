from internals.objects import Page, Form, Field, Cookie, CookieSource, ReferencedObject
from bs4 import BeautifulSoup

import requests
import time

from internals.handlers import eventhandler


def get_content_type(url):
    response = requests.head(url)
    return response.headers['Content-Type']


class Scrapper:
    @staticmethod
    def scrap(soup: BeautifulSoup, address: str, cookies: dict) -> Page:
        start_time = time.time()
        eventhandler.new_status(f"Scrappring {address} ...")
        # get title
        title = soup.find("title").string

        # get links
        eventhandler.new_status("Scrapping links")
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
                    eventhandler.new_info(f"Link {link} that was expected to lead to a file leads to a page instead")
                    links.append(link)
                else:
                    eventhandler.new_info(f'Link {link} leads to a file ({guessed_type})')
                    objects.append(ReferencedObject(
                        link=link,
                        object_type=guessed_type,
                    ))
            else:
                eventhandler.new_info(f"Link {link} leads to a page")
                links.append(link)
        eventhandler.new_status("Successfully found all links")

        # get forms
        eventhandler.new_status("Scrapping forms")
        forms = list()
        eventhandler.new_status("Forms successfully scrapped")

        # get cookies
        eventhandler.new_status("Scrapping cookies")
        cookie_sources = list()
        for source in cookies:
            cookies_list = list()
            for key, value in source.items():
                cookies_list.append(Cookie(key, value))
            cookie_sources.append(CookieSource(cookies_list))
        eventhandler.new_status("Successfully loaded all cookies")

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
        eventhandler.new_status(f"Successfully scrapped page at {address} in {round(time.time() - start_time, 3)} seconds")
        return page

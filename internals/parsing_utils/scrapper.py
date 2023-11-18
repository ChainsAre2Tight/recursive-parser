from internals.objects import Page, Form, Field, Cookie, CookieSource, ReferencedObject
from bs4 import BeautifulSoup

import requests
import time
import urllib.parse

from internals.handlers import eventhandler
from internals.exceptions import PageCouldntBeReachedError
from internals.timeout import timeout, MyTimeout


@timeout(2)
def get_content_type(url):
    try:
        response = requests.head(url)
        return response.headers['Content-Type']
    except MyTimeout as er:
        raise er
    except Exception as er:
        raise PageCouldntBeReachedError(er.args)


class Scrapper:
    @staticmethod
    def scrap(soup: BeautifulSoup, address: str, cookies: dict, known_links: dict[str]) -> Page:
        start_time = time.time()
        eventhandler.new_status(f"Scrappring {address} ...")
        # get title
        try:
            title = soup.find("title").string
        except AttributeError:
            title = 'No title found'

        # get links
        eventhandler.new_status("Scrapping links")
        all_links = list(map(lambda x: x['href'], soup.find_all(href=True)))
        links = list()
        objects = list()
        unreachable = list()
        for link in all_links:
            try:
                if link[:4] != 'http' and link[0] == '/':
                    link = urllib.parse.urljoin(address, link)
            except IndexError:
                continue

            if 0 or (link.count('/') >= 3 and link.rfind('.') > link.rfind('/') and link[-4:] not in [".php", 'html']):

                if link not in known_links.keys():
                    guessed_type = 'Unknown/'
                    try:
                        guessed_type = get_content_type(link)
                        if type(guessed_type) == PageCouldntBeReachedError:
                            guessed_type = 'Unknown/Unreachable'
                    except PageCouldntBeReachedError:
                        eventhandler.new_error(f"Couldn't reach {link}. Skipping")
                        guessed_type = 'Unknown/Unreachable'
                    except MyTimeout:
                        eventhandler.new_error(f"Reached timeout wile trying to access {link}. Skipping")
                        guessed_type = 'Unknown/Timeout'
                    known_links[link] = guessed_type
                else:
                    guessed_type = known_links[link]

                if 'text/html' in guessed_type:
                    eventhandler.new_info(
                        f"Link {link} that was expected to lead to a file leads to a page instead")
                    links.append(link)
                elif "Unknown" not in guessed_type:
                    eventhandler.new_info(f'Link {link} leads to a file ({guessed_type})')
                    objects.append(ReferencedObject(
                        link=link,
                        object_type=guessed_type,
                    ))
                else:
                    eventhandler.new_info(f"Link {link} couldn't be reached ({guessed_type})")
                    unreachable.append(ReferencedObject(
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
            unreachable=unreachable,
        )

        # return it
        eventhandler.new_status(
            f"Successfully scrapped page at {address} in {round(time.time() - start_time, 3)} seconds")
        return page

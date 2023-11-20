from internals.objects import *


def strip_string(string_to_strip: str, stripper: str) -> str:
    if string_to_strip[:len(stripper)] == stripper:
        return string_to_strip[len(stripper):]
    return string_to_strip


def strip_link(link: str) -> str:
    link = strip_string(link, 'https://')  # get rid of https://
    link = strip_string(link, 'http://')  # get rid of http://
    link = strip_string(link, 'www.')  # get rid of www.
    return link


def transform(link: str) -> str:
    """
    :param link: link to transform
    :return: link without https://, www. and everything behind domain address
    """
    link = strip_link(link)
    link = link.split('/')[0]  # get only domain
    return link


def get_directory(link: str) -> str:
    link = strip_link(link)
    linkArray = link.split('/')
    link = ''
    domain_flag = False
    for part in linkArray:
        if '.' in part and domain_flag:
            link = link + '/'
            break
        elif '.' in part:
            domain_flag = True
        link = link + '/' + part

    link = link[1:]
    if link.count('/') > 0:
        linkArray = link.split('/')
        link = '/'.join(linkArray[:-1])

    return link


def exclude_subdomains(link: str) -> str:
    link = transform(link)

    if link.count('.') > 1:
        link = '.'.join(link.split('.')[-2:])  # get rid of subdomains

    return link


def same_domain(link1: str, link2: str) -> bool:
    """Checks if both links lead to the same domain e.g. uk.example.com == us.example.com"""
    return exclude_subdomains(link1) == exclude_subdomains(link2)


def same_website(link1: str, link2: str) -> bool:
    """Checks if both links lead to the same website e.g. uk.example.com != example.com"""
    return transform(link1) == transform(link2)


def strip_GET_from_link(link: str) -> str:
    if '?' in link:
        link = link[:link.find('?')]
    return link


def strip_all_get_params(parsed_pages: dict) -> dict:
    result = dict()

    pages = list(parsed_pages.keys())
    for i in range(len(pages)):
        page = pages[i]
        page_was_stripped = False

        # rename node itself
        new_name = strip_GET_from_link(page)
        if new_name != page:
            page_was_stripped = True

        if type(parsed_pages[page]) == str:
            result[page] = new_name
            continue

        # Begin constructing new Page object
        new_page: Page
        self: Page = parsed_pages[page]

        # rename all links
        new_links = set()
        for link in parsed_pages[page].links:
            new_links.add(strip_GET_from_link(link))

        # merge with other pages
        # TODO move this to Page class
        merged_title = self.title
        merged_address = self.address
        merged_links = list(new_links)
        merged_cookies = self.cookies
        merged_objects = self.objects
        merged_forms = self.forms

        merged_unreachable = list()
        for unreachable in self.unreachable:
            merged_unreachable.append(
                ReferencedObject(
                    object_type=unreachable.object_type,
                    link=strip_GET_from_link(unreachable.link)
                )
            )

        # merged_unreachable = self.unreachable
        if new_name in result.keys() and type(result[new_name]) == Page:
            other: Page = result[new_name]

            merged_title = other.title
            merged_address = other.address
            merged_links = list(set(other.links).union(new_links))
            merged_cookies = other.cookies
            merged_objects = other.objects
            merged_forms = list(set(other.forms).union(set(self.forms)))

            def merge_referenced_object(obj1: ReferencedObject, obj2: ReferencedObject) -> list[ReferencedObject]:
                if obj1.object_type == obj2.object_type and strip_GET_from_link(obj1.link) == strip_GET_from_link(
                        obj2.link):
                    return [obj1]
                return [obj1, obj2]

            merged_unreachable = list()
            for obj1 in other.unreachable:
                for obj2 in self.unreachable:
                    merged_unreachable.extend(merge_referenced_object(obj1, obj2))

        new_page = Page(
            title=f"{'Merged @ ' if page_was_stripped and 'Merged @' not in merged_title else ''}{merged_title}",
            address=merged_address,  # TODO add flag that page was altered so to recolor it on graph
            links=merged_links,
            cookies=merged_cookies,
            objects=merged_objects,
            forms=merged_forms,
            unreachable=merged_unreachable,
        )

        result[new_name] = new_page

    return result


if __name__ == "__main__":
    # print(get_directory('https://example.com/index.php'))
    # print(get_directory('https://example.com/clo/index.php'))
    # print(get_directory('https://example.com/aboba/'))
    # print(get_directory('https://example.com/aboba'))
    # print(get_directory('https://example.com/'))
    # print(get_directory('https://example.com/r.php?r=https://lox.com'))
    # print(get_directory('https://example.com/aboba/index.php/lox'))
    # print(get_directory('https://example.com/aboba/lox/pidr/index.php'))
    # print(
    #     get_directory(get_directory('https://example.com/aboba/lox/pidr/index.php'))
    # )
    # print(
    #     get_directory('example.com')
    # )
    print(strip_GET_from_link(
        'https://example.com/r.php?r=https://lox.com'
        ''))

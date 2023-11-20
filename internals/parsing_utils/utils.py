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


if __name__ == "__main__":
    print(get_directory('https://example.com/index.php'))
    print(get_directory('https://example.com/clo/index.php'))
    print(get_directory('https://example.com/aboba/'))
    print(get_directory('https://example.com/aboba'))
    print(get_directory('https://example.com/'))
    print(get_directory('https://example.com/r.php?r=https://lox.com'))
    print(get_directory('https://example.com/aboba/index.php/lox'))
    print(get_directory('https://example.com/aboba/lox/pidr/index.php'))
    print(
        get_directory(get_directory('https://example.com/aboba/lox/pidr/index.php'))
    )
    print(
        get_directory('example.com')
    )

def transform(link: str) -> str:
    """
    :param link: link to transform
    :return: link without https://, www. and everything behind domain address
    """
    link = link[link.find('/') + 2:]  # get rid of http:// and http://
    link = link.strip('www.')  # get rid of www.
    link = link.split('/')[0]  # get only domain
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


from dataclasses import dataclass


@dataclass
class Field:
    name: str  # name of a field
    field_type: str  # type of the field
    validations: str  # validations of said field


@dataclass
class Form:
    method: str  # GET or POST
    fields: list[Field]  # list of fields


@dataclass
class Cookie:
    name: str  # name of the cookie
    value: str  # value of the cookie


@dataclass
class CookieSource:
    cookies: list[Cookie]


@dataclass
class ReferencedObject:
    link: str
    object_type: str


@dataclass
class Page:
    title: str  # Title of said page
    address: str  # link to this page
    forms: list[Form]  # list of forms that are found on a page
    cookies: list[CookieSource]  # list of cookies that are found on a page
    links: list[str]  # list of links to other pages that are found on a page
    objects: list[ReferencedObject]  # list of all objects that are referenced on a page (eg. /static/img.png)
    unreachable: list[ReferencedObject]  # links that cannot be accessed

    def to_html(self):
        return f'''{str(self)}'''

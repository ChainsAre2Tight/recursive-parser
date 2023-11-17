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
class Page:
    title: str  # Title of said page
    address: str  # link to this page
    forms: list[Form]  # list of forms that are found on a page
    cookies: list[Cookie]  # list of cookies that are found on a page
    links: list[str]  # list of links to other pages that are found on a page

import json
from dataclasses import dataclass


@dataclass
class Action:
    """
    An array of hashes identifying the actions this campaign links to on its public page.
    """

    title: str
    browser_url: str


@dataclass
class Link:
    """
    A link to this individual campaign resource.
    """

    href: str


@dataclass
class SelfLink:
    self: Link


@dataclass
class NextLink:
    next: Link


@dataclass
class PageLinks:
    next: NextLink
    self: SelfLink


@dataclass
class Campaign:
    identifiers: list[str]
    created_date: str
    modified_date: str
    description: str
    featured_image_url: str
    browser_url: str
    title: str
    actions: list[Action]
    _links: SelfLink


@dataclass
class Emebedded:
    data: list[Campaign]


@dataclass
class Page:
    total_pages: int
    per_page: int
    page: int
    total_records: int
    _links: PageLinks
    _embedded: Emebedded

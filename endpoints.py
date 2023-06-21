from dataclasses import dataclass

from .base import Action, Link


@dataclass
class Campaign:
    identifiers: list[str]
    created_date: str
    modified_date: str
    description: str
    title: str
    actions: list[Action]
    _links: list[Link]
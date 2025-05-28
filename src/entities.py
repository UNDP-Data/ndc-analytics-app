"""
Entities (data models) for managing search, chat and filter options.
"""

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from xml.etree.ElementTree import Element

from pandas import to_datetime
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, computed_field

__all__ = [
    "Engine",
    "Category",
    "Geography",
    "Request",
    "Passage",
    "Avatar",
    "Message",
    "FeedItem",
]


class Engine(StrEnum):
    """
    Enumerator for search engine options.
    """

    FULLTEXT_EN = "Full-text search (English)"
    # FULLTEXT_FR = "Full-text search (French)"
    # FULLTEXT_ES = "Full-text search (Spanish)"
    NEURAL = "Neural search"


class Category(StrEnum):
    """
    Enumerator for categoty options.
    """

    ACCESS = "Energy access"
    TRANSITION = "Energy transition"
    RESILIENCE = "Energy resilience"
    EFFICIENCY = "Energy efficiency"
    RENEWABLE = "Renewable energy"


class Geography(StrEnum):
    """
    Enumerator for geographical scope options.
    """

    ALL = "All countries"
    CP1 = "CP1 countries"
    CP2 = "CP2 countries"
    CUSTOM = "Specific countries"


class Request(BaseModel):
    """
    Search request data model containing settings and filters.
    """

    model_config = ConfigDict(populate_by_name=True)

    engine: Engine
    query: str | list[float] = Field(
        description="Query string or vector", alias="user_message"
    )
    geography: str
    category: str | None = None
    version: int | None = None
    dates: tuple[datetime, datetime]


class Passage(BaseModel):
    """
    Passage data model for a chunk of an NDC.
    """

    iso: str
    party: str
    version: int
    date: datetime
    type: Literal["original", "translation"]
    title: str
    url: AnyUrl
    file_name: str
    language: str
    text: str
    pages: list[int]
    vector: list[float]

    @computed_field
    @property
    def citation(self) -> str:
        """
        Computed property to get a user-friendly citation of the passage.

        Returns
        -------
        str
            User-friendly citation of the passage.
        """
        # add one because pages are zero-indexed in the database
        if len(self.pages) > 1:
            page = f"pp. {self.pages[0] + 1}-{self.pages[-1] + 1}"
        else:
            page = f"p. {self.pages[0] + 1}"
        url = f"{self.url}#page={self.pages[0] + 1}"
        citation = f"[{self.title}]({url}), {page} {self.date.year}"
        return citation

    def to_context(self) -> dict:
        """
        Convert the passage to a context dictionary.

        Returns
        -------
        dict
            Dictionary containing passage text and source for citation.
        """
        return {
            "source": self.citation,
            "text": self.text,
        }


class Avatar(StrEnum):
    """
    Enumerator for chat avatars.
    """

    ASSISTANT = ":material/psychology:"
    USER = ":material/person:"


class Message(BaseModel):
    """
    Chat message model.
    """

    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
        description="Timestamp of the message",
    )
    role: Literal["assistant", "user"]
    content: str

    def __lt__(self, other):
        """
        Enable message sorting by timestamp from oldest to newest.
        """
        return self.timestamp < other.timestamp

    @property
    def icon(self) -> str:
        """
        Convenience property for displaying a message icon.

        Returns
        -------
        str
            Icon from the Material Symbols library.
        """
        return str(Avatar[self.role.upper()])


class FeedItem(BaseModel):
    """
    Feed item from NDC Registry RSS.
    """

    guid: str = Field(description="Unique identifier of the item.")
    title: str = Field(description="Title of the item.")
    link: AnyUrl = Field(description="Link to the item.")
    description: str = Field(description="Detailed description of the item.")
    date: datetime = Field(description="Date the item was published.")
    creator: str = Field(description="Creator of the item.")

    @classmethod
    def from_xml(cls, item: Element, namespaces: dict) -> "FeedItem":
        """
        Create a FeedItem from an XML element.
        Parameters
        ----------
        item : Element
            XML element to parse the item from.
        namespaces : dict
            Dictionary of namespace URIs.

        Returns
        -------
        FeedItem
            Parsed FeedItem from the XML element.
        """
        return cls(
            guid=item.find("guid").text,
            title=item.find("title").text,
            link=item.find("link").text,
            description=item.find("description").text,
            # e.g. "Thu, 13 Jun 2024 12:00:00 +0000"
            date=to_datetime(item.find("pubDate").text),
            creator=item.find("dc:creator", namespaces).text,
        )

    @property
    def header(self) -> str:
        """
        Get a user-friendly header for this Feed item to display as an expander title.

        Returns
        -------
        str
            User-friendly header for the item.
        """
        return f"{self.title} ({self.date:%a, %d %b %Y})"

    @property
    def body(self) -> str:
        """
        Get a user-friendly text body for this Feed item to display as a text within the expander.

        Returns
        -------
        str
            User-friendly text body for the item.
        """
        rows = [
            f"Link: {self.link}",
            # e.g., "Party: Panama<br /> Version: 3<br /> Status: Active"
            *self.description.split("<br />"),
            f"Creator: {self.creator}",
        ]
        return "\n\n".join(rows)

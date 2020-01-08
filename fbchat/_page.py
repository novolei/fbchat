import attr
from ._core import attrs_default, Image
from . import _session, _plan
from ._thread import Thread


@attrs_default
class Page(Thread):
    """Represents a Facebook page. Inherits `Thread`."""

    #: The session to use when making requests.
    session = attr.ib(type=_session.Session)
    #: The unique identifier of the page.
    id = attr.ib(converter=str)
    #: The page's picture
    photo = attr.ib(None)
    #: The name of the page
    name = attr.ib(None)
    #: Datetime when the thread was last active / when the last message was sent
    last_active = attr.ib(None)
    #: Number of messages in the thread
    message_count = attr.ib(None)
    #: Set `Plan`
    plan = attr.ib(None)
    #: The page's custom URL
    url = attr.ib(None)
    #: The name of the page's location city
    city = attr.ib(None)
    #: Amount of likes the page has
    likes = attr.ib(None)
    #: Some extra information about the page
    sub_title = attr.ib(None)
    #: The page's category
    category = attr.ib(None)

    @classmethod
    def _from_graphql(cls, session, data):
        if data.get("profile_picture") is None:
            data["profile_picture"] = {}
        if data.get("city") is None:
            data["city"] = {}
        plan = None
        if data.get("event_reminders") and data["event_reminders"].get("nodes"):
            plan = _plan.Plan._from_graphql(data["event_reminders"]["nodes"][0])

        return cls(
            session=session,
            id=data["id"],
            url=data.get("url"),
            city=data.get("city").get("name"),
            category=data.get("category_type"),
            photo=Image._from_uri(data["profile_picture"]),
            name=data.get("name"),
            message_count=data.get("messages_count"),
            plan=plan,
        )

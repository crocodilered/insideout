from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, Boolean, Text, Date
from webapp.libs.mediahelper import MediaHelper


Base = declarative_base()


class Event(Base):
    __tablename__ = "event"
    event_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    date = Column("dt", Date, nullable=False)
    enabled = Column(Boolean)

    def __init__(self, event_id=None, title=None, text=None, date=None, enabled=None):
        Base.__init__(self)
        self.event_id = event_id
        self.title = title
        self.text = text
        self.date = date
        self.enabled = enabled

    @property
    def photo(self):
        return MediaHelper.event_media_uri(self.event_id)

    @property
    def uri(self):
        return MediaHelper.event_uri(self.event_id)

    @property
    def date_f(self):
        r = None
        if self.date:
            r = self.date.strftime("%d.%m.%Y")
        return r

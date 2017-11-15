from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, Boolean, Text, Date
from webapp.libs.mediahelper import MediaHelper


Base = declarative_base()


class Schedule(Base):
    __tablename__ = "schedule"
    schedule_id = Column(Integer, primary_key=True)
    date = Column("dt", Date, nullable=False)
    content = Column(Text, nullable=False)
    enabled = Column(Boolean)

    def __init__(self, schedule_id=None, date=None, content=None, enabled=None):
        Base.__init__(self)
        self.schedule_id = schedule_id
        self.date = date
        self.content = content
        self.enabled = enabled

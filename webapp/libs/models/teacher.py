from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, Boolean, Text
from webapp.libs.mediahelper import MediaHelper

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teacher"
    teacher_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    col1 = Column(Text, nullable=False)
    col2 = Column(Text, nullable=False)
    sortkey = Column(Integer, nullable=False)
    enabled = Column(Boolean)

    def __init__(self, teacher_id=None, name=None, col1=None, col2=None, sortkey=None, enabled=None):
        Base.__init__(self)
        self.teacher_id = teacher_id
        self.name = name
        self.col1 = col1
        self.col2 = col2
        self.sortkey = sortkey
        self.enabled = enabled

    @property
    def photo(self):
        return MediaHelper.teacher_media_uri(self.teacher_id)

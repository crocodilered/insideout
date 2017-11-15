from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, Boolean


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(36))
    enabled = Column(Boolean)

    def __init__(self, login, password, enabled):
        Base.__init__(self)
        self.login = login
        self.password = password
        self.enabled = enabled

    @staticmethod
    def list(session):
        r = session.query(User).all()
        return r

    @staticmethod
    def get_by_credentials(session, login, password):
        r = None
        if login and password:
            data = session.query(User) \
                .filter(User.login == login) \
                .filter(User.password == password)
            if data.count():
                r = data[0]
        return r

    @staticmethod
    def get_by_token(session, token):
        r = None
        if token:
            data = session.query(User) \
                .filter(User.token == token)
            if data.count():
                r = data[0]
        return r

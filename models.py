from sqlalchemy import ForeignKey, String, Integer, create_engine
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase, sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

from typing import List, Optional, Dict

class Base(DeclarativeBase):
    pass

class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    master: Mapped[bool] = mapped_column(Integer, nullable=False, default=0)

    def __init__(self, site: str, password: str, username: Optional[str] = None, email: Optional[str] = None, master: Optional[bool] = False):
        if not master:
            self.site = site
            self.username = username
            self.email = email
            self.password = password
        else:
            self.site = site
            self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<Site(site='{self.site}', email='{self.email}', username='{self.username}')>"
    
    def decode(self) -> Dict[str, str]:
        result = {}
        result["site"] = self.site
        result["username"] = self.username
        result["email"] = self.email
        result["password"] = self.password
        return result

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_master(cls, session: Session):
        return session.query(cls).filter(cls.master == 1).first()


def get_session() -> Session:
    engine = create_engine("sqlite:///data.db")
    if not database_exists(engine.url):
        create_database(engine.url)
    
    Base.metadata.create_all(bind=engine)

    Session_current = sessionmaker(bind=engine)
    session_current = Session_current()
    return session_current

def setup_database():
    engine = create_engine("sqlite:///data.db", echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    
    Base.metadata.create_all(bind=engine)

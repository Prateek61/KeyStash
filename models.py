from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

from typing import List, Optional, Dict

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    master: Mapped[bool] = mapped_column(Integer, nullable=False, default=0)

    def __init__(self, site: str, password: str, username: str = None, master: Optional[bool] = False):
        self.site = site
        self.username = username
        self.master = master
        self.password = password

    def __repr__(self):
        return f"<Site(site='{self.site}', email='{self.username}', username='{self.username}')>"

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from cryptography.fernet import Fernet

from typing import List, Optional, Dict

class Base(DeclarativeBase):
    pass

class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(self, site: str, password: str, fernet_engine: Fernet, username: Optional[str] = None, email: Optional[str] = None):
        self.site = fernet_engine.encrypt(password.encode())
        self.username = fernet_engine.encrypt(username.encode()) if username else None
        self.email = fernet_engine.encrypt(email.encode()) if email else None
        self.password = fernet_engine.encrypt(password.encode())

    def __repr__(self):
        return f"<Site(site='{self.site}', email='{self.email}', username='{self.username}')>"
    
    def decrypt(self, fernet_engine: Fernet) -> Dict[str, Optional[str]]:
        result = dict()
        result["site"] = fernet_engine.decrypt(self.site).decode()
        result["username"] = fernet_engine.decrypt(self.username).decode() if self.username else None
        result["email"] = fernet_engine.decrypt(self.email).decode() if self.email else None
        result["password"] = fernet_engine.decrypt(self.password).decode()


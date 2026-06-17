from sqlalchemy import Column, Integer, String
from .database import Base

class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    owner = Column(String)
    last_updated = Column(String)

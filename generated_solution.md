### FILE: app/models.py
```python
from sqlalchemy import Column, Integer, String
from .database import Base

class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    owner = Column(String)
    last_updated = Column(String)
```

### FILE: graphql_schema.py
```python
from strawberry import auto
from strawberry.types import Info
from . import models, database
from typing import List
from fastapi import Depends

class Query:
    @auto
    def repos(self, info: Info) -> List[models.Repo]:
        db = database.SessionLocal()
        return db.query(models.Repo).all()

    @auto
    def microsoft_repos(self, info: Info, per_page: int = auto(), page: int = auto()) -> dict:
        db = database.SessionLocal()
        offset = (page - 1) * per_page
        return {
            "repos": db.query(models.Repo).offset(offset).limit(per_page).all(),
            "pagination": {"page": page, "per_page": per_page},
        }

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

schema = auto(
    Query,
    resolvers={
        Query.repos: Query.repos,
        Query.microsoft_repos: Query.microsoft_repos,
    },
)
```
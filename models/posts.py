from config.database import Base
from sqlalchemy import Column, Integer, String


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)

from config.database import Base, engine
import models.posts


def add_db():
    Base.metadata.create_all(bind=engine)

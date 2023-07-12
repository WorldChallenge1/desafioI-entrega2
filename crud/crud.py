from sqlalchemy.orm import Session
from models.posts import Post as PostModel
from schemas.posts import Post


def get_posts(db: Session):
    return db.query(PostModel).all()


def get_post(db: Session, id: int):
    return db.query(PostModel).filter(PostModel.id == id).first()


def create_post(db: Session, post: Post):
    db_post = PostModel(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, id: int, post: Post):
    db.query(PostModel).filter(PostModel.id == id).update(post.model_dump())
    db.commit()


def delete_post(db: Session, id: int):
    db.query(PostModel).filter(PostModel.id == id).delete()
    db.commit()

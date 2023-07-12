from fastapi import FastAPI, Response, status, Depends
from schemas.posts import Post as PostSchema
from config.database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
import crud.crud as crud
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts(response: Response, db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    if not posts:
        response.status_code = status.HTTP_204_NO_CONTENT
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostSchema, db: Session = Depends(get_db)):
    created_post = crud.create_post(db, post)
    return created_post


# , response_model=PostSchema
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = crud.get_post(db, id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    return post


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(
    id: int, updated_post: PostSchema, response: Response, db: Session = Depends(get_db)
):
    if id != updated_post.id:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Post id does not match"}
    post = crud.get_post(db, id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    crud.update_post(db, id, updated_post)
    return


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = crud.get_post(db, id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    crud.delete_post(db, id)
    return


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

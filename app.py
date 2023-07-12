from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db
from schemas.posts import Post as PostSchema
from typing import List
import os
import crud.crud as crud

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ.get("DATABASE_URL"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[PostSchema])
async def get_posts(response: Response):
    posts = crud.get_posts(db.session)
    if not posts:
        response.status_code = status.HTTP_204_NO_CONTENT
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post(post: PostSchema, response: Response):
    created_post = crud.create_post(db.session, post)
    response.headers["Location"] = f"/posts/{created_post.id}"
    return created_post


@app.get(
    "/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostSchema | dict
)
async def get_post(id: int, response: Response):
    post = crud.get_post(db.session, id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    return post


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, updated_post: PostSchema, response: Response):
    if id != updated_post.id:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Post id does not match"}
    post = crud.get_post(db.session, id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    crud.update_post(db.session, id, updated_post)
    return


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
    post = crud.get_post(db.session, id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    crud.delete_post(db.session, id)
    return


# if __name__ == "__main__":
#     uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

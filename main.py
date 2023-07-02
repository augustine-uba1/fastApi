from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!!"}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Posts):
    post_dict = post.dict()
    post_dict['id'] = randrange(100, 10000000)
    my_posts.append(post_dict)
    print(my_posts)
    return{"data": post_dict}

@app.get("/post/{id}")
def get_post(id : int):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    return{"post detail": post}
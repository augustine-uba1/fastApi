from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Welcome to my api!!!"}

@app.get("/feeds")
def feeds():
    return {"Feeds" : "Here is a list of feeds"}

# getting both parameters without pydantic
# @app.posts("/createfeed")
# def create_feed(payload: dict = Body(...)):
#     print(payload)
#     return{"new feed": f"feed title: {payload['title']}, content: {payload['content']}"}

@app.post("/createposts")
def create_posts(posts : Posts):
    print(posts.rating, posts.published)
    print(posts.dict())
    return{"data": posts}
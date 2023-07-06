from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
import psycopg
import time

import models
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
while True:    
    try:
        conn = psycopg.connect(host="localhost", port="5432", dbname="fastapi",
        user="postgres", password="Certly20231234$")
        
        cursor = conn.cursor()
        print("connection to database successful!!!!")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error:", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    
@app.get("/")
async def root():
    return {"message": "Welcome to my api!!!"}

# TRYING TO USE SQLALCHEMY
@app.get("/sqlqlchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "Successful"}
    

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Posts):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES
                   (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    print(my_posts)
    conn.commit()
    return{"data": new_post}

# MAKE A POST
@app.get("/post/{id}")
def get_post(id : int):
    dab_id = id
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,)) 
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    return{"post detail": post}

# DELETE A POST 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    deleted_post = cursor.fetchone()
    conn.commit()    
    if deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Posts):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
                   WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    
    return {"data" : updated_post}
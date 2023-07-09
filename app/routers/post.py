from typing import List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

import models, schemas, oauth2
from database import get_db




router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

# GET ALL POSTS
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return posts

# CREATE A POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
                 user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES
    #                (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # print(my_posts)
    # conn.commit()
    
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# GET A POST BY ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db), 
             user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,)) 
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    
    return post

# DELETE A POST 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), 
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
        
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A POST
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
    #                WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # post = post_query.first()
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {post_query.first()}
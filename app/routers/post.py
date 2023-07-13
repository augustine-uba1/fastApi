from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import func
import app.models, app.schemas, app.oauth2
from app.database import get_db




router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

# GET ALL POSTS
@router.get("/", response_model=List[app.schemas.PostOut])

def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(app.oauth2.get_current_user), limit: int = 2, 
              skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # RETURNING POSTS WITH LIKES
    posts = db.query(app.models.Post, func.count(app.models.Vote.post_id).label("votes")).join(
        app.models.Vote, app.models.Vote.post_id == app.models.Post.id, isouter=True).group_by(
            app.models.Post.id).filter(app.models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

# CREATE A POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=app.schemas.Post)
def create_posts(post : app.schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(app.oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES
    #                (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # print(my_posts)
    # conn.commit()
    
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    print(current_user.email)
    new_post = app.models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# GET A POST BY ID
@router.get("/{id}", response_model=app.schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), 
             current_user: int = Depends(app.oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,)) 
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(app.models.Post, func.count(app.models.Vote.post_id).label("votes")).join(
        app.models.Vote, app.models.Vote.post_id == app.models.Post.id, isouter=True).group_by(
            app.models.Post.id).filter(app.models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    
    # print   (post.owner.email)
    # RETRIEVE ONLY CURRENT LOGGED IN USERS POST
    if post.Post.owner_id  !=  current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorised to perform this action")   
    
    return post

# DELETE A POST 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), 
                current_user: int = Depends(app.oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = post = db.query(app.models.Post).filter(app.models.Post.id == id)
    post = post_query.first()
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorised to perform this action")    
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE A POST
@router.put("/{id}", response_model= app.schemas.Post)
def update_post(id: int, updated_post: app.schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(app.oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
    #                WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(app.models.Post).filter(app.models.Post.id == id)
    # post = post_query.first()
    
    post = post_query.first()
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorised to perform this action") 
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit() 
    return post_query.first()
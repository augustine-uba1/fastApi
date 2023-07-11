from fastapi import  FastAPI






import models
from database import engine
from routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


    
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
        
        
        
        
        
        










# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title": "title of post 2", "content": "content of post 2", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
    
# @app.get("/")
# async def root():
#     return {"message": "Welcome to my api!!!"}

# TRYING TO USE SQLALCHEMY
# @app.get("/sqlqlchemy")
# def test_posts(db: Session = Depends(get_db)):
    
#     posts = db.query(models.Post).all()
#     return {"data" : posts}
    
# # GET ALL POSTS
# @app.get("/posts", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db)):
#     # cursor.execute(""" SELECT * FROM posts""")
#     # posts = cursor.fetchall()
#     posts = db.query(models.Post).all()
#     print(posts)
#     return posts

# # CREATE A POST
# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES
#     #                (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # print(my_posts)
#     # conn.commit()
    
#     # new_post = models.Post(title = post.title, content = post.content, published = post.published)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
    
#     return new_post

# # GET A POST BY ID
# @app.get("/post/{id}", response_model=schemas.Post)
# def get_post(id : int, db: Session = Depends(get_db)):
#     # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,)) 
#     # post = cursor.fetchone()
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id {id} was not found")
    
#     return post

# # DELETE A POST 
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id : int, db: Session = Depends(get_db)):
#     # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
#     # deleted_post = cursor.fetchone()
#     # conn.commit()
#     post = post = db.query(models.Post).filter(models.Post.id == id)
    
#     if not post.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id {id} does not exist")
        
#     post.delete(synchronize_session=False)
#     db.commit()
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # UPDATE A POST
# @app.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
#     #                WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    
#     # updated_post = cursor.fetchone()
#     # conn.commit()
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     # post = post_query.first()
    
#     if not post_query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id {id} does not exist")
    
#     post_query.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return {post_query.first()}

# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):
    
#     # hash user password in user.password
#     harshed_password = utils.hash(user.password)
#     user.password = harshed_password
#     new_user = models.Users(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return new_user


# @app.get("/users/{id}", response_model=schemas.UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == id).first()
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"User with id: {id} not found")
#     return user
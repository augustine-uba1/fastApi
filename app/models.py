from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from app.database import Base

# from database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable=False)
    
    owner = relationship("Users")
    
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)
    
class Vote(Base):
    __tablename__ = "votes"
    user_id= Column(Integer, ForeignKey(column="users.id", ondelete= "CASCADE"), primary_key= True)
    post_id= Column(Integer, ForeignKey(column="posts.id", ondelete= "CASCADE"), primary_key= True)
    
    
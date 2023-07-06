from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UpdatePost(PostBase):
    published: bool
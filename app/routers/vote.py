from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session

import app.models, app.schemas, app.oauth2
from app.database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: app.schemas.Vote, db: Session = Depends(get_db), 
         current_user: int = Depends(app.oauth2.get_current_user)):
    
    post = db.query(app.models.Post).filter(app.models.Post == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {vote.post_id} not found")
    vote_query = db.query(app.models.Vote).filter(app.models.Vote.post_id == vote.post_id,
                                              app.models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()   
    # applying logic for direction for voting (1 = like, 0 = unlike)
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= f"user {current_user.email} has already voted for this post of {vote.post_id}")
        new_vote = app.models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "successfully voted"} 
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()  
        return{"message": "successfully deleted vote"}  
    
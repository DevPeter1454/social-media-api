from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    first_vote = vote_query.first()
    if vote.dir == 1:
        if first_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id) 
        db.add(new_vote)

        db.commit()
        return {"detail": "Vote updated successfully"}
        
    else:
        if first_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not voted yet")
        vote_query.delete(synchronize_session=False)
        db.commit()  
        return {"detail": "Vote removed successfully"}  
    # if(vote.dir == 1):
    #     .update({"dir": 1}, synchronize_session=False)
    # else:
    #     db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).update({"dir": -1}, synchronize_session=False)
    # db.commit()
    # db.refresh(vote)
    # return vote
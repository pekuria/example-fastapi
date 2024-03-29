from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from app import models, schemas, utils, oauth2
from app.database import get_db

router = APIRouter(prefix="/votes",
                   tags=["votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote
                , db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist")
    
    vote_query =  db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    
    if(current_user.id == post.owner_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user can not vote for own post")

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
       
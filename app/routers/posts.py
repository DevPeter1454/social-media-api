from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import engine, get_db
from sqlalchemy import func, desc

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/all", status_code= status.HTTP_200_OK )
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip:int = 10, search: Optional[str] = ""):
    """get all posts"""
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return  posts
    
@router.post("/create-post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(user_id = current_user.id,**post.model_dump())
   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post
    
@router.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_user_post(current_user = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    
    return  posts

    
@router.get("/{id}", status_code=status.HTTP_200_OK,  response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return  post
    
    

@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate , db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    first_post = post_query.first()
    if first_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if first_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
    
    
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
     
    post_query.delete(synchronize_session=False)
    db.commit()
    
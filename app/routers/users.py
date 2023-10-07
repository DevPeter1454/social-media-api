from .. import models, schemas, utils
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password
    old_user = db.query(models.User).filter(models.User.email == user.email).first()
    if old_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    user.password = utils.hash(user.password)
        
    new_user = models.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return  new_user
    

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    return  user
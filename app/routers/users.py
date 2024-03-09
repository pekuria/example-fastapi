from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from app import models, schemas, utils, oauth2
from app.database import get_db

router = APIRouter(prefix="/users",
                   tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} not found")
    return user


@router.get("/", response_model=list[schemas.UserOut])
def get_user(db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).all()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users in the users table")
    return user

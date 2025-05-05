from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from .. import schemas, models
from .. database import get_db
from .. hashing import hash_password


router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)) -> models.User:
    hashed_password = hash_password(request.password)
    request.password = hashed_password
    new_user = models.User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)) -> models.User:
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user


@router.get('/', response_model=List[schemas.ShowUser], tags=['Users'])
def get_all_users(db: Session = Depends(get_db)) -> List[models.User]:
    users = db.query(models.User).all()
    return users
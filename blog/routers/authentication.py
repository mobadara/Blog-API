from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models
from .. hashing import verify_password
  

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not verify_password(request.password, str(user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    
    return {'message': 'Login successful'}


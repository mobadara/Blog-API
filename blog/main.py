from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext   

from .database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()                  


from . import schemas, models
from .database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['Blogs'])                
def create(request: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:    
    new_blog = models.Blog(**request.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def destroy(id: int, db: Session = Depends(get_db)) -> None:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    db.delete(blog)
    db.commit()
    return None

@app.patch('/blog/{id}', response_model=schemas.ShowBlog, status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    for key, value in request.model_dump().items():
        setattr(blog, key, value)
    db.commit()
    db.refresh(blog)
    return blog
    
     
@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blogs'])
def all(db: Session = Depends(get_db)) -> List[models.Blog]:
    blogs = db.query(models.Blog).all()
    return blogs
    
    
@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['Blogs'])
def show(id: int, db: Session = Depends(get_db)) -> models.Blog:       
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')   
    return blog


@app.post('/user', response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)) -> models.User:
    hashed_password = pwd_context.hash(request.password)
    request.password = hashed_password
    new_user = models.User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)) -> models.User:
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user


@app.get('/user', response_model=List[schemas.ShowUser], tags=['Users'])
def get_all_users(db: Session = Depends(get_db)) -> List[models.User]:
    users = db.query(models.User).all()
    return users
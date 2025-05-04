from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List        

from .database import SessionLocal

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

@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)                
def create(request: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:    
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)) -> None:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    db.delete(blog)
    db.commit()
    return None

@app.patch('/blog/{id}', response_model=schemas.ShowBlog)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    for key, value in request.model_dump().items():
        setattr(blog, key, value)
    db.commit()
    db.refresh(blog)
    return blog
    
    
        
    
@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)) -> List[models.Blog]:
    blogs = db.query(models.Blog).all()
    return blogs
    
    
@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)) -> models.Blog:       
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')   
    return blog
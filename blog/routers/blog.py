from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from .. import schemas, models
from .. database import get_db

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)                
def create(request: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:    
    new_blog = models.Blog(**request.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)) -> None:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    db.delete(blog)
    db.commit()
    return None

@router.patch('/{id}', response_model=schemas.ShowBlog, status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)) -> models.Blog:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    for key, value in request.model_dump().items():
        setattr(blog, key, value)
    db.commit()
    db.refresh(blog)
    return blog
    
     
@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)) -> List[models.Blog]:
    blogs = db.query(models.Blog).all()
    return blogs
    
    
@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)) -> models.Blog:       
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')   
    return blog

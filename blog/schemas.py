from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: Optional[str]
    body: Optional[str]
    published: Optional[bool] = False
    
class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    published: bool
    
    class Config:
        from_attributes = True
        
        
# User schemaas
class User(BaseModel):
    username: str
    email: str
    password: str
    

class ShowUser(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True
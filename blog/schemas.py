from pydantic import BaseModel
from typing import List
from typing import List, Optional

# Blog schema for the POST request
class Blog(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True

# Schema for User input (to be used in POST requests)
class User(BaseModel):
    name: str
    email: str
    password: str 

# Schema for displaying user data (without password)
class Showuser(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        from_attributes = True

# Schema for displaying blog data
class showBlog(BaseModel):
    id: int
    title: str
    body: str
    owner: Showuser

    class Config:
        from_attributes = True  # This is important for Pydantic to convert ORM objects to JSON
        

class login(BaseModel):
    username:str
    password:str


    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email: Optional[str]=None
from pydantic import BaseModel

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

    class Config:
        orm_mode = True 

# Blog schema for the POST request
class Blog(BaseModel):
    title: str
    body: str

# Schema for displaying blog data
class showBlog(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        orm_mode = True  # This is important for Pydantic to convert ORM objects to JSON

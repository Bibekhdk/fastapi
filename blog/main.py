from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import blog,user , authentication

#create db tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()





# Include routers
app.include_router(authentication.router)

app.include_router(blog.router)

app.include_router(user.router)
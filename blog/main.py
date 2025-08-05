from fastapi import FastAPI
from . import models
from .database import engine 
from .routers import blog,user , authentication
from fastapi.middleware.cors import CORSMiddleware


#create db tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods: GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)




# Include routers
app.include_router(authentication.router)

app.include_router(blog.router)

app.include_router(user.router)
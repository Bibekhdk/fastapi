from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from .database import engine, SessionLocal
from  .hashing import Hash


app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing setup with passlib
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to hash password
def hash_password(password: str):
    return pwd_cxt.hash(password)

# Create Blog
@app.post("/blog", status_code=201,tags=['blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Delete Blog
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted successfully"}

# Update Blog
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return {"detail": "Updated successfully"}

# Get all blogs
@app.get('/blog',tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# Get blog by ID
@app.get('/blog/{id}', status_code=200, response_model=schemas.showBlog,tags=['blogs'])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    return blog

# Create User
@app.post('/user', response_model=schemas.Showuser,tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    print(f"Original password: {request.password}")  # Log original password
    hashed_password = hash_password(request.password)
    print(f"Hashed password: {hashed_password}")  # Log the hashed password
    
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user 


@app.get('/user/{id}',response_model=schemas.Showuser,tags=['users'])
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    return user 
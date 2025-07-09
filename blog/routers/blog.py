from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session, joinedload  # Import joinedload
from .. import schemas, database, models
from typing import List
from ..repository import blog   
get_db=database.get_db

router = APIRouter(
    tags=['blogs'],
    prefix='/blog'
)




@router.get('/', response_model=List[schemas.showBlog])
def all(db: Session = Depends(get_db)):   
    return blog.get_all(db) 




@router.post("/", status_code=201)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request,db)




@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return blog.destroy(id,db)




@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id,request,db)




@router.get('/{id}', status_code=200, response_model=schemas.showBlog)
def show(id: int, db: Session = Depends(get_db)):
   return blog.show(id,db )
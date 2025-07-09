from fastapi import APIRouter,Depends
from .. import database,schemas
from sqlalchemy.orm import Session
from ..repository import user

get_db = database.get_db

router=APIRouter(
    tags=['users'],
    prefix='/user'

)

@router.post('/', response_model=schemas.Showuser)
def create(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/{id}', response_model=schemas.Showuser)
def get(id: int, db: Session = Depends(get_db)):
    return user.get(id,db)

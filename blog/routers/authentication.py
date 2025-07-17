from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash  # ✅ make sure you import your Hash helper

router = APIRouter(tags=['authentication'])


@router.post('/login')
def login(request: schemas.login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    # ✅ Verify password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Invalid password")
    
    return  user

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, token
from ..hashing import Hash
from datetime import timedelta
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=['authentication'])

@router.post('/login', response_model=schemas.Token)
def login(
    request: OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Invalid password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = token.create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer"
    )

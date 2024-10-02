from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, services, auth, database

router = APIRouter()

@router.post("/register", response_model=schemas.UserBalance)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if services.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return services.create_user(db, user)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Implement endpoints for deposit, withdraw, transfer with authentication
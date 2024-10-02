# app/api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, auth
from .database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                   (user.username, auth.get_password_hash(user.password)))
    db.commit()
    return schemas.User(id=cursor.lastrowid, username=user.username, balance=0.0)

@router.post("/token", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()
    
    if not db_user or not auth.verify_password(user.password, db_user[2]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/deposit")
def deposit(amount: float, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    
    cursor = db.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, current_user.id))
    db.commit()
    return {"message": "Deposit successful", "balance": current_user.balance + amount}

@router.post("/withdraw")
def withdraw(amount: float, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")
    
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (current_user.id,))
    balance = cursor.fetchone()[0]
    
    if amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, current_user.id))
    db.commit()
    return {"message": "Withdrawal successful", "balance": balance - amount}

@router.post("/transfer")
def transfer(to_account: str, amount: float, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")
    
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (current_user.id,))
    balance = cursor.fetchone()[0]
    
    if amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    cursor.execute("SELECT * FROM users WHERE username = ?", (to_account,))
    recipient = cursor.fetchone()
    
    if recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, current_user.id))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, recipient[0]))
    db.commit()
    return {"message": "Transfer successful", "balance": balance - amount}


@router.get("/user/details")
def get_user_details(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Use raw SQL query to get the user balance and details
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, username, balance FROM users WHERE id = ?", (current_user.id,))
        user_data = cursor.fetchone()

        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_details = {
            "id": user_data[0],
            "username": user_data[1],
            "balance": user_data[2]
        }

        return user_details
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching user details")
    finally:
        cursor.close()
    
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas, database, auth
from sqlalchemy import func

router = APIRouter()

@router.post("/deposit/", response_model=schemas.TransactionResponse)
def deposit(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    
    db_transaction = models.Transaction(amount=transaction.amount, type="deposit", user_id=current_user.id)
    current_user.balance += transaction.amount
    db.add_all([current_user, db_transaction])
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.post("/withdraw/", response_model=schemas.TransactionResponse)
def withdraw(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")
    if current_user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    db_transaction = models.Transaction(amount=-transaction.amount, type="withdrawal", user_id=current_user.id)
    current_user.balance -= transaction.amount
    db.add_all([current_user, db_transaction])
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.post("/transfer/", response_model=schemas.TransactionResponse)
def transfer(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")
    recipient = db.query(models.User).filter(models.User.account_number == transaction.recipient_account_number).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    if current_user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Using database locks could be more robust for concurrency but for simplicity:
    db.execute("LOCK TABLES users WRITE;")
    try:
        current_user.balance -= transaction.amount
        recipient.balance += transaction.amount
        db_transaction = models.Transaction(amount=-transaction.amount, type="transfer", user_id=current_user.id, recipient_account_number=recipient.account_number)
        db.add_all([current_user, recipient, db_transaction])
        db.commit()
    finally:
        db.execute("UNLOCK TABLES;")
    db.refresh(db_transaction)
    return db_transaction
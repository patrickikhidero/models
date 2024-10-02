from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    account_number = Column(String, unique=True)
    balance = Column(Float, default=0.0)

    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    recipient_account = Column(String, nullable=True)

    user = relationship("User", back_populates="transactions")
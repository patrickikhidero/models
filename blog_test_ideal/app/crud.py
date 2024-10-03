from sqlalchemy.orm import Session
from . import models, schemas

def create_blog_post(db: Session, post: schemas.BlogPostCreate):
    db_post = models.BlogPost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_blog_post(db: Session, post_id: int):
    return db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()

def get_blog_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BlogPost).offset(skip).limit(limit).all()

def update_blog_post(db: Session, post_id: int, post: schemas.BlogPostUpdate):
    db_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    if db_post:
        update_data = post.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_blog_post(db: Session, post_id: int):
    db_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
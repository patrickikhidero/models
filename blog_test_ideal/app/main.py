from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/posts/", response_model=schemas.BlogPost)
def create_post(post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    return crud.create_blog_post(db=db, post=post)

@app.get("/posts/", response_model=list[schemas.BlogPost])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_blog_posts(db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=schemas.BlogPost)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_blog_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{post_id}", response_model=schemas.BlogPost)
def update_post(post_id: int, post: schemas.BlogPostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_blog_post(db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}", response_model=schemas.BlogPost)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_blog_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
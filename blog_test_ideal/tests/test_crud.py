from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_blog_post(db: Session):
    post = schemas.BlogPostCreate(title="Test Post", content="This is a test post")
    db_post = crud.create_blog_post(db, post)
    assert db_post.title == "Test Post"
    assert db_post.content == "This is a test post"
    assert db_post.id is not None

def test_get_blog_post(db: Session):
    post = schemas.BlogPostCreate(title="Test Post", content="This is a test post")
    db_post = crud.create_blog_post(db, post)
    
    retrieved_post = crud.get_blog_post(db, post_id=db_post.id)
    assert retrieved_post.title == "Test Post"
    assert retrieved_post.content == "This is a test post"
    assert retrieved_post.id == db_post.id

def test_get_blog_posts(db: Session):
    post1 = schemas.BlogPostCreate(title="Test Post 1", content="This is test post 1")
    post2 = schemas.BlogPostCreate(title="Test Post 2", content="This is test post 2")
    crud.create_blog_post(db, post1)
    crud.create_blog_post(db, post2)
    
    posts = crud.get_blog_posts(db)
    assert len(posts) == 2
    assert posts[0].title == "Test Post 1"
    assert posts[1].title == "Test Post 2"

def test_update_blog_post(db: Session):
    post = schemas.BlogPostCreate(title="Test Post", content="This is a test post")
    db_post = crud.create_blog_post(db, post)
    update_data = schemas.BlogPostUpdate(title="Updated Post", content="This is an updated post")
    updated_post = crud.update_blog_post(db, db_post.id, update_data)
    
    assert updated_post.title == "Updated Post"
    assert updated_post.content == "This is an updated post"
    assert updated_post.id == db_post.id

def test_delete_blog_post(db: Session):
    post = schemas.BlogPostCreate(title="Test Post", content="This is a test post")
    db_post = crud.create_blog_post(db, post)
    
    deleted_post = crud.delete_blog_post(db, db_post.id)
    assert deleted_post.id == db_post.id
    
    retrieved_post = crud.get_blog_post(db, db_post.id)
    assert retrieved_post is None
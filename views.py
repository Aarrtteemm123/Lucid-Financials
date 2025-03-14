from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from functools import lru_cache
from starlette.requests import Request
from helpers import hash_password, create_access_token, login_required
from models import User, Post, get_db
from schemas import UserCreate, PostCreate

class LoginView:

    def signup(self, request: Request, user: UserCreate, db: Session = Depends(get_db)):
        hashed_password = hash_password(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}


    def login(self, request: Request, user: UserCreate, db: Session = Depends(get_db)):
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or db_user.hashed_password != hash_password(user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user.email})
        return {"token": token}


class PostView:

    @login_required
    def add_post(self, request: Request, post: PostCreate, db: Session = Depends(get_db)):
        user = request.state.user
        db_post = Post(user_id=user.id, text=post.text)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return {"postID": db_post.id}

    @lru_cache(maxsize=128)
    @login_required
    def get_posts(self, request: Request, db: Session = Depends(get_db)):
        user = request.state.user
        posts = db.query(Post).filter(Post.user_id == user.id).all()
        return posts

    @login_required
    def delete_post(self, request: Request, postID: int, db: Session = Depends(get_db)):
        user = request.state.user
        post = db.query(Post).filter(Post.id == postID, Post.user_id == user.id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}

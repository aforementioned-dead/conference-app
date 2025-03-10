from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import UserBase


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    try:
        existing_user = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail=f"Пользователь с именем '{user.username}' уже существует.")
        
        db_user = models.User(username=user.username, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка уникальности: пользователь с именем '{user.username}' уже существует.")


def update_user(db: Session, user_id: int, updated_user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db_user.username = updated_user.username
    db_user.role = updated_user.role
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(db_user)
    db.commit()
    return {"detail": "Пользователь успешно удален"}


def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return user
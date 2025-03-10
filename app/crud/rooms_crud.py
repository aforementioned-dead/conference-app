from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.base import Room


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room_id: int, updated_room: schemas.RoomCreate):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    db_room.name = updated_room.name
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    db.delete(db_room)
    db.commit()
    return {"detail": "Комната успешно удалена"}


def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()
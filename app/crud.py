from sqlalchemy.orm import Session
from app import models, schemas
from collections import defaultdict
from sqlalchemy import and_
from datetime import datetime
from fastapi import HTTPException

def get_rooms(db: Session):
    return db.query(models.Room).all()


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_presentation(db: Session):
    return db.query(models.Presentation).all()


def create_presentation(db: Session, presentation: schemas.PresentationCreate):
    db_presentation = models.Presentation(
        title=presentation.title,
        description=presentation.description,
        presenter=presentation.presenter
    )
    db.add(db_presentation)
    db.commit()
    db.refresh(db_presentation)
    return db_presentation


def get_schedules(db: Session):
    return db.query(models.Schedule).all()


# def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
#     db_schedule = models.Schedule(
#         room_id=schedule.room_id, 
#         presentation_id=schedule.presentation_id,
#         start_time=schedule.start_time,
#         end_time=schedule.end_time
#     )
#     db.add(db_schedule)
#     db.commit()
#     db.refresh(db_schedule)
#     return db_schedule


def get_schedule_by_room(db: Session):
    schedules = db.query(models.Schedule).all()
    result = defaultdict(list)
    for schedule in schedules:
        room = db.query(models.Room).filter(models.Room.id == schedule.room_id).first()
        presentation = db.query(models.Presentation).filter(models.Presentation.id == schedule.presentation_id).first()
        result[room.name].append({
            "presentations": presentation.title,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time
        })
    return result


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    overlapping = db.query(models.Schedule).filter(
        and_(
            models.Schedule.room_id == schedule.room_id,
            models.Schedule.end_time > schedule.start_time,
            models.Schedule.start_time < schedule.end_time
        )
    ).first()

    if overlapping:
        raise HTTPException(status_code=400, detail="Это время уже занято другой презентацией. Пожалуйста, выберите другое время!")
    
    db_schedule = models.Schedule(
        room_id=schedule.room_id,
        presentation_id=schedule.presentation_id,
        start_time=schedule.start_time,
        end_time=schedule.end_time
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule
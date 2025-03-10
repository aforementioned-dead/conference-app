from sqlalchemy.orm import Session
from app import models, schemas
from collections import defaultdict
from sqlalchemy import and_
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import Depends


def get_users(db: Session):
    return db.query(models.User).all()


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
    try:
        existing_user = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail=f"Пользователь с именем '{user.username}' уже существует."
            )
        
        db_user = models.User(username=user.username, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка уникальности: пользователь с именем '{user.username}' уже существует."
        )


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


def update_presentation(db: Session, presentation_id: int, updated_presentation: schemas.PresentationCreate):
    db_presentation = db.query(models.Presentation).filter(models.Presentation.id == presentation_id).first()
    if not db_presentation:
        raise HTTPException(status_code=404, detail="Презентация не найдена")

    db_presentation.title = updated_presentation.title
    db_presentation.description = updated_presentation.description
    db_presentation.presenter = updated_presentation.presenter
    db.commit()
    db.refresh(db_presentation)
    return db_presentation


def delete_presentation(db: Session, presentation_id: int):
    db_presentation = db.query(models.Presentation).filter(models.Presentation.id == presentation_id).first()
    if not db_presentation:
        raise HTTPException(status_code=404, detail="Презентация не найдена")
    
    db.delete(db_presentation)
    db.commit()
    return {"detail": "Презентация успешно удалена"}


def update_schedule(db: Session, schedule_id: int, updated_schedule: schemas.ScheduleCreate):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    overlapping = db.query(models.Schedule).filter(
        and_(
            models.Schedule.room_id == updated_schedule.room_id,
            models.Schedule.end_time > updated_schedule.start_time,
            models.Schedule.start_time < updated_schedule.end_time,
            models.Schedule.id != schedule_id
        )
    ).first()

    if overlapping:
        raise HTTPException(status_code=400, detail="Это время уже занято другой презентацией. Пожалуйста, выберите другое время!")
    
    db_schedule.room_id = updated_schedule.room_id
    db_schedule.presentation_id = updated_schedule.presentation_id
    db_schedule.start_time = updated_schedule.start_time
    db_schedule.end_time = updated_schedule.end_time
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_schedule(db: Session, schedule_id: int):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")
    
    db.delete(db_schedule)
    db.commit()
    return {"detail": "Расписание успешно удалено"}


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
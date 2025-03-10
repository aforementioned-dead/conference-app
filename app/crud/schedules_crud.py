from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from collections import defaultdict


def get_schedules(db: Session):
    return db.query(models.Schedule).all()


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
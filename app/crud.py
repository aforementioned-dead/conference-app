from sqlalchemy.orm import Session
from app import models, schemas


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


def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
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


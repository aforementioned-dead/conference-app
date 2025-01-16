from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Комнаты", "description": "Управление аудиториями."},
    {"name": "Презентации", "description": "Управление докладами."},
    {"name": "Расписания", "description": "Управление расписанием."},
    {"name": "Пользователи", "description": "Управление пользователями."},
]

app = FastAPI(title="Менеджер конференций", description="API для управления конференциями", openapi_tags=tags_metadata)


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в менеджер конференций"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/rooms/{room_id}", response_model=schemas.Room, tags=["Комнаты"])
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    return room


@app.post("/rooms", response_model=schemas.Room, tags=["Комнаты"])
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)


@app.get("/presentations", response_model=list[schemas.Presentation], tags=["Презентации"])
def read_presentations(db: Session = Depends(get_db)):
    return crud.get_presentation(db)


@app.post("/presentations", response_model=schemas.Presentation, tags=["Презентации"])
def create_presentation(presentation: schemas.PresentationCreate, db: Session = Depends(get_db)):
    return crud.create_presentation(db, presentation)


@app.get("/schedules", response_model=list[schemas.Schedule], tags=["Расписания"])
def read_schedules(db: Session = Depends(get_db)):
    return crud.get_schedules(db)


@app.post("/schedules", response_model=schemas.Schedule, tags=["Расписания"])
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_schedule(db, schedule)


@app.get("/schedule-by-room", tags=["Расписания"])
def read_schedule_by_room(db: Session = Depends(get_db)):
    return crud.get_schedule_by_room(db)


@app.post("/users", response_model=schemas.User, tags=["Пользователи"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.put("/rooms/{room_id}", response_model=schemas.Room, tags=["Комнаты"])
def update_room(room_id: int, updated_room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.update_room(db, room_id, updated_room)


@app.delete("/rooms/{room_id}", tags=["Комнаты"])
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return crud.delete_room(db, room_id)


@app.put("/presentations/{presentation_id}", response_model=schemas.Presentation, tags=["Презентации"])
def update_presentation(presentation_id: int, updated_presentation: schemas.PresentationCreate, db: Session = Depends(get_db)):
    return crud.update_presentation(db, presentation_id, updated_presentation)


@app.delete("/presentations/{presentation_id}", tags=["Презентации"])
def delete_presentation(presentation_id: int, db: Session = Depends(get_db)):
    return crud.delete_presentation(db, presentation_id)


@app.put("/schedules/{schedule_id}", response_model=schemas.Schedule, tags=["Расписания"])
def update_schedule(schedule_id: int, updated_schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.update_schedule(db, schedule_id, updated_schedule)


@app.delete("/schedules/{schedule_id}", tags=["Расписания"])
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    return crud.delete_schedule(db, schedule_id)


@app.put("/users/{user_id}", response_model=schemas.User, tags=["Пользователи"])
def update_user(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, updated_user)


@app.delete("/users/{user_id}", tags=["Пользователи"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


@app.get("/users", tags=["Пользователи"])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
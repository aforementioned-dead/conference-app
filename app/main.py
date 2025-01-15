from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в менеджер конференций"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/rooms", response_model=list[schemas.Room])
def read_rooms(db: Session = Depends(get_db)):
    return crud.get_rooms(db)

@app.post("/rooms", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)

@app.get("/presentations", response_model=list[schemas.Presentation])
def read_presentations(db: Session = Depends(get_db)):
    return crud.get_presentations(db)

@app.post("/presentations", response_model=schemas.Presentation)
def create_presentation(presentation: schemas.PresentationCreate, db: Session = Depends(get_db)):
    return crud.create_presentation(db, presentation)

@app.get("/schedules", response_model=list[schemas.Schedule])
def read_schedules(db: Session = Depends(get_db)):
    return crud.get_schedules(db)

@app.post("/schedules", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_schedule(db, schedule)


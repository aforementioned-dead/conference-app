from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from collections import defaultdict


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

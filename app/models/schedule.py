from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    presentation_id = Column(Integer, ForeignKey("presentations.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    room = relationship("Room", back_populates="schedules")
    presentation = relationship("Presentation", back_populates="schedules")
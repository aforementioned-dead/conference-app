from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    schedules = relationship("Schedule", back_populates="room")


class Presentation(Base):
    __tablename__ = "presentations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    presenter = Column(String)

    schedules = relationship("Schedule", back_populates="presentation")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    presentation_id = Column(Integer, ForeignKey("presentations.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    room = relationship("Room", back_populates="schedules")
    presentation = relationship("Presentation", back_populates="schedules")

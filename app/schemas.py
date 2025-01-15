from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        from_attributes = True


class PresentationBase(BaseModel):
    title: str
    description: Optional[str] = None
    presenter: str

class PresentationCreate(PresentationBase):
    pass

class Presentation(PresentationBase):
    id: int

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    room_id: int
    presentation_id: int
    start_time: datetime
    end_time: datetime

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    role: str


class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
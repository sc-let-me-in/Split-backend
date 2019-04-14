import enum

from sqlalchemy import Column, String, ForeignKey, Date, Enum, Float, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Household(Base):
    __tablename__ = "household"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(256), nullable=False)
    utilities = relationship("Utility", backref="household")
    users = relationship("User", backref="household")
    rooms = relationship("Room", backref="household")


class Utility(Base):
    __tablename__ = "utility"

    id = Column(Integer, primary_key=True, nullable=False)
    household_id = Column(Integer, ForeignKey('household.id'))
    name = Column(String(length=256), nullable=False)
    cost = Column(Float, nullable=False, default=0)
    due_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    household_id = Column(Integer, ForeignKey('household.id'))
    room_id = Column(Integer, ForeignKey("room.id"))
    in_charge_of = relationship("Utility", backref="user_in_charge")
    name = Column(String(length=256), nullable=False)
    email = Column(String(length=256), nullable=False)
    password = Column(String(length=256), nullable=False)
    leader = Column(Boolean, default=False, nullable=False)
    venmo = Column(String(length=256), nullable=False)


class RoomType(enum.Enum):
    bed_room = 0
    common_room = 1


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, nullable=False)
    household_id = Column(Integer, ForeignKey('household.id'))
    users = relationship("User", backref="rooms")
    type = Column(Enum(RoomType), nullable=False)
    size = Column(Float, nullable=False, default=0)

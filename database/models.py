from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    apps = relationship("App", backref="user")


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, index=True)
    image = Column(String)
    description = Column(String, default="No Description")
    switch = Column(String)
    volume = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    ports = relationship("Port", backref="app",cascade="all,delete")

class Port(Base):
    __tablename__ = "ports"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    pod_port = Column(Integer)
    user_port = Column(Integer)
    app_id = Column(Integer,ForeignKey("apps.id"))


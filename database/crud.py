from sqlalchemy.orm import Session
from sqlalchemy import and_ ,or_
import hashlib
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha256(bytes(user.password,'utf-8')).hexdigest()
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_app(db: Session, app: schemas.AppCreate, user_id: int):
    app_dict = app.dict()
    ports = []

    for key in list(app_dict):
        if key == "ports":
            ports = app_dict[key]
            del app_dict[key]

    db_app = models.App(**app_dict, owner_id=user_id)
    for port in ports:
        db_app.ports.append(models.Port(**port))
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def check_user_app(db: Session,app_name: str,user_id:int):
    db_app = db.query(models.App).filter(and_(models.App.name == app_name,models.App.owner_id == user_id)).first()
    return db_app is not None 

def delet_user_app(db: Session,user_id:int,app_id:int):
    db_app = db.query(models.App).filter(and_(models.App.id == app_id,models.App.owner_id == user_id)).first()
    if db_app is not None:
        db.delete(db_app)
        db.commit()
        return db_app
    return False

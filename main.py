from fastapi import FastAPI, Depends ,HTTPException
from datetime import datetime
import dockerFunctions as dockfunc
from database import crud, models, schemas
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"status":datetime.now()}


@app.post("/api/users/",response_model=schemas.User)
def register(user: schemas.UserCreate,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already Exists")
    return crud.create_user(db=db,user=user)

@app.get("/api/users/{user_id}",response_model=schemas.User)
def profile(user_id:int,db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/api/users/{user_id}/apps/",response_model=schemas.App)
def create_app(app: schemas.AppCreate,user_id: int,db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    dockfunc.createContainer(app=app,user_email=db_user.email)
    app_exists = crud.check_user_app(db=db,app_name=app.name,user_id=user_id)
    if(app_exists):
        raise HTTPException(status_code=400, detail="App Already Exists")
    return crud.create_user_app(db=db,app=app,user_id=user_id)

@app.get("/api/users/{user_id}/apps/",response_model=list[schemas.App])
def user_apps(user_id:int,db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.apps

@app.delete("/api/users/{user_id}/apps/{app_id}",response_model=schemas.App)
def delete_app(user_id:int,app_id:int,db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_app = crud.delet_user_app(db=db,user_id=user_id,app_id=app_id)
    if db_app is False:
        raise HTTPException(status_code=404, detail="App record not found")
    return db_app


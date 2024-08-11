from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from app.users import routes as user_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/users", tags=["users"])

"""@app.post("/ping")
def test_ping():
    return {"message": "Hello World"}

@app.post("/createstudent", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_user  = crud.get_student(db, student_sid=student.sid)

    if db_user:
        raise HTTPException(status_code=400, detail="Student ID Already Exist")
    
    return crud.create_student(db=db, student=student)

@app.post("/createsession", response_model=schemas.SessionBase)
def create_session(session: schemas.SessionBase, db: Session = Depends(get_db)):
    return crud.create_session(db=db, session=session)

@app.post("/createreservation", response_model=schemas.LockerReservationBase)
def create_reservation(session: schemas.LockerReservationBase, db: Session = Depends(get_db)):
    return crud.create_lockerreservation(db=db, session=session)"""
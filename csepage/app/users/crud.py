from sqlalchemy.orm import Session

import app.users.models as models
import app.users.schemas as schemas

def get_student(db: Session, student_sid: int):
    return db.query(models.Student).filter(models.Student.sid == student_sid).first()

def get_name(db: Session, grade: int):
    return db.query(models.Student).filter(models.Student.grade == grade).first()

def create_student(db: Session, student: schemas.StudentCreate) -> None:
    default_password = student.birth.strftime('%y%m%d') # default password set password = Birth(YYMMDD)

    new_student = models.Student(
        sid = student.sid,
        name = student.name,
        gender = student.gender,
        grade = student.grade,
        phone = student.phone,
        birth = student.birth,
        email = student.email,
        password = default_password,
        nickname = student.nickname,
        auth = student.auth
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

def create_session(db: Session, session: schemas.SessionBase) -> None:
    new_session = models.Session(
        uuid = session.uuid,
        sid = session.sid
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
def get_session(db: Session, session_uuid: str) -> models.Session:
    """세션 ID로 세션을 가져오는 함수"""
    return db.query(models.Session).filter(models.Session.uuid == session_uuid).first()

def get_student_by_username(db: Session, username: str) -> models.Student:
    """사용자 이름으로 학생을 조회하는 함수 (username을 student의 sid로 가정)"""
    return db.query(models.Student).filter(models.Student.sid == username).first()
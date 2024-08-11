from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import validates

from database import Base

class Student(Base):
    __tablename__ = "students"

    sid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String)
    grade = Column(Integer)
    phone = Column(String)
    birth = Column(Date)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False) # default birth(YYMMDD)
    nickname = Column(String)
    auth = Column(Integer, nullable=False)

    @validates('gender')
    def validate_gender(self, key, gender):
        '''성별 제한 확인 함수
        '''
        if gender is not None:
            if gender not in ("male", "female"):
                raise ValueError("gender must be male or female")

        return gender

    @validates('birth')
    def default_password(self, key, birth):
        '''비밀번호 기본값 설정 함수
        '''
        self.password = birth.strftime('%y%m%d')

        return birth

    @validates('auth')
    def validate_auth(self, key, auth):
        '''권한 제한 확인 함수
        '''
        if auth not in (0, 1, 2):
            raise ValueError("auth must be 0(normal), 1(professor), 2(admin)")
        
        return auth

class Session(Base):
    __tablename__ = "sessions"

    uuid = Column(String, nullable=False, primary_key=True)
    sid = Column(Integer, ForeignKey("students.sid")) # FK
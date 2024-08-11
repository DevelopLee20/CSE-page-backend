from fastapi import HTTPException, Depends, status, Cookie, APIRouter
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Optional
import bcrypt

from dependency import get_db
import app.users.crud as crud
import app.users.schemas as schemas

router = APIRouter()

def generate_session_id():
    return str(uuid4())

async def get_user(session_id: str, db: Session = Depends(get_db)):
    # 세션 ID로 세션 조회
    session = crud.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="세션이 유효하지 않습니다.")
    
    return crud.get_student(db, session.sid)

@router.post("/login/")
async def login(login_data: schemas.LoginRequest, session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    # 쿠키에 세션 ID가 존재하는지 확인
    if session_id:
        try:
            user = await get_user(session_id, db)
            return {"message": "세션이 유효합니다.", "user_id": user.sid}
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="세션이 유효하지 않습니다. 로그인이 필요합니다.")

    # login_data에서 sid 및 password 가져오기
    sid = login_data.sid
    password = login_data.password

    # sid로 사용자 조회
    student = crud.get_student(db, sid)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    # 비밀번호 검증
    if not bcrypt.checkpw(password.encode('utf-8'), student.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="비밀번호가 일치하지 않습니다.")

    # 세션 생성
    new_session_id = generate_session_id()
    crud.create_session(db, schemas.SessionBase(uuid=new_session_id, sid=student.sid))
    
    # 쿠키로 세션 ID를 전달
    response = {"message": "로그인 성공", "session_id": new_session_id}
    cookie = f"session_id={new_session_id}; Path=/; HttpOnly"
    
    return response, {"headers": {"Set-Cookie": cookie}}
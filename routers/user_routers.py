from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data.conf.db_session import get_session
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from service import user_service

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def list_users(session: Session = Depends(get_session)):
    return user_service.get_all(session)


@router.get("/user/{cs}", response_model=UserResponse)
def list_by_cs(cs: int, session: Session = Depends(get_session)):
    try:
        return user_service.get_user_by_cs(session, cs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/user_create", response_model=UserCreate)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    try:
        return user_service.post_user(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# está atualiuzando os outros campos mesma não enviando eles
@router.patch("/user_update/{cs}", response_model=UserResponse)
def update_user(
    cs: int, data: UserUpdate, session: Session = Depends(get_session)
):
    try:
        return user_service.update_user(session, cs, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

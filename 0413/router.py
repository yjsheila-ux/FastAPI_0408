from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete

from database.connection import get_session
from database.connection_async import get_async_session
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse


#user 핸들러 함수들을 관리하는 객체
router = APIRouter(tags=["User"])
                    #prefix="/users"

@router.get(
        "/users", 
        summary="전체 사용자 조회 API",
        status_code=status.HTTP_200_OK,
        response_model=list[UserResponse],
)
async def get_users_handler(
    # Depends: FastAPI 에서 의존성(get_session)을 자동으로 실행/주입/정리
    session = Depends(get_async_session),
):
    # statement = 구문(명령문)
    stmt =select(User) # SELECT * FROM user;
    result = await session.execute(stmt)
    users = result.scalars().all() # 객체로 변경 [user1, user2,...] 데이터 찾기 편함.
                # mapping() 은 dict 형태로 
    return users


@router.get(
        "/users/search",
        summary="사용자 정보 검색 API",
        response_model=list[UserResponse],
)
async def search_users_handler(
    name: str | None = Query(None),  # 타입힌트로 기본값을 none 으로 할당.
    job: str | None = Query(None),
    session = Depends(get_async_session),
):
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다."
        )

    stmt = select(User)
    if name:
        stmt = stmt.where(User.name == name)
    if job:
        stmt = stmt.where(User.job == job)

    result = await session.execute(stmt)
    users = result.scalar().all()
    return users

# 단일 사용자 API {user_id} 사용자 데이터 조회
@router.get(
        "/users/{user_id}",
        summary="단일 사용자 데이터 조회 API", # 주석을 summary 안으로
        response_model=UserResponse,
)
async def get_user_handler(
    user_id: int = Path(..., ge=1), 
    session = Depends(get_async_session),
):  
    # SELECT * FROM user WHERE id =42;
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar() # 존재하면 user객체, 존재하지 않으면 None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found", # 존재하지 않는 유저는 404
        ) 
    return user

# 메소드 = POST , 경로 = 메소드/users

@router.post(
        "/users",
        summary="회원 가입(추가) API",
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse,
)
async def create_user_handler(
    # 1) 사용자 데이터를 받는다 + 데이터 유효성 검사
    body: UserCreateRequest,
    session = Depends(get_async_session),
):
    new_user  = User(name=body.name, job=body.job) #클래스로 생성
    session.add(new_user)
    print(new_user.id, new_user.created_at) # none
    await session.commit() # 변경사항 저장
    await session.refresh(new_user) # db 동기화 - id, created_at
    print(new_user.id, new_user.created_at) # value
    return new_user


@router.patch(
        "/users/{user_id}",
        summary= "회원 정보 수정 API",
        response_model=UserResponse,
)
async def update_user_handler(
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_async_session),
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
    
    user.job = body.job
    # session.add(user)
    await session.commit() # job 상태(job 변경)를 db에 반영
        # e.g. UPDATE user SET job = '  ' WHERE user.id = 1;

# 회원 삭제 API
# DELETE//users/{user_id}
@router.delete(
        "/users/{user_id}",
        summary="회원 삭제 API",
        status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_handler(
    user_id: int,
    session = Depends(get_async_session),
):
# 1) get + delete
#   user 조회 후 삭제 
# 2) delete
#   delete 10 user -> 있으면 삭제, 없으면 무시
    
    # # 1) user 조회 후 삭제 
    # with SessionFactory() as session:
    #     stmt = select(User).where(User.id == user_id)
    #     result = await session.execute(stmt)
    #     user = result.scalar()

    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="User Not Found",
    #         )
    
    #     await session.delete(user) # 실제 객체(데이터)를 삭제
    #     # session.expunge(user) -> 세션의 추적대상에서 제거
    #     await session.commit()

    # 2) 곧 바로 삭제
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()

# await
# session.execute()
# session.commit()
# session.refesh()

from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete

from database.connection import get_session
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse
# 강사님 코드 -> user 폴더 안으로 파일을 옮겼더니 바뀜.👍
# from request import UserCreateRequest
# from response import UserResponse

#user 핸들러 함수들을 관리하는 객체
router = APIRouter(tags=["User"])
                    #prefix="/users"

@router.get(
        "/users", 
        summary="전체 사용자 조회 API",
        status_code=status.HTTP_200_OK,
        response_model=list[UserResponse],
)
def get_users_handler(
    # Depends: FastAPI 에서 의존성(get_session)을 자동으로 실행/주입/정리
    session = Depends(get_session),
):
    # statement = 구문(명령문)
    stmt =select(User) # SELECT * FROM user;
    result = session.execute(stmt)
    users = result.scalars().all() # 객체로 변경 [user1, user2,...] 데이터 찾기 편함.
    return users

# 사용자 정보 검색 API
# GET/ /users/search?name=alex
# GET/ /users/search?job=student
@router.get(
        "/users/search",
        summary="사용자 정보 검색 API",
        response_model=list[UserResponse],
)
def search_users_handler(
    name: str | None = Query(None),  # 타입힌트로 기본값을 none 으로 할당.
    job: str | None = Query(None),
    session = Depends(get_session),
):
    # 1) name O / job X
    # 2) name X / job O
    # 3) name X / job X
    # 4) name O / job O
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다."
        )

    stmt = select(User)
    if name:
        stmt = stmt.where(User.name == name)
        # stmt = select(User).where(User.name == name)
    if job:
        stmt = stmt.where(User.job == job)
        # 1) name을 거쳐온 경우
        # stmt = select(User).where(User.name == name).where(User.job == job)
        # 2) name을 안 거친 경우 
        # stmt = stmt.where(User.job == job)

    result = session.execute(stmt)
    users = result.scalar().all()
    return users

# 단일 사용자 API {user_id} 사용자 데이터 조회
@router.get(
        "/users/{user_id}",
        summary="단일 사용자 데이터 조회 API", # 주석을 summary 안으로
        response_model=UserResponse,
)
def get_user_handler(
    user_id: int = Path(..., ge=1), 
    session = Depends(get_session),
):  
    # SELECT * FROM user WHERE id =42;
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    # scalars() -> 첫번째 열의 데이터만 가져온다
    # all() -> 리스트로 변환
    # result.scalars().all()
    user = result.scalar() # 존재하면 user객체, 존재하지 않으면 None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found", # 존재하지 않는 유저는 404
        ) 
    return user

# 회원 가입(추가) API
# 메소드 = POST , 경로 = 메소드/users

@router.post(
        "/users",
        summary="회원 가입(추가) API",
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse,
)
def create_user_handler(
    # 1) 사용자 데이터를 받는다 + 데이터 유효성 검사
    body: UserCreateRequest,
    session = Depends(get_session),
):
# try:
    new_user  = User(name=body.name, job=body.job) #클래스로 생성
    session.add(new_user)
    session.commit() # 변경사항 저장
    session.refresh(new_user) # db 동기화 - id, created_at
    return new_user
# finally:
#     session.close()

# 회원 정보 수정 API
# PUT : 전체 교체 (replace)
# PATCH : 일부 수정 (pa)
# PATCH/users/{user_id}
@router.patch(
        "/users/{user_id}",
        summary= "회원 정보 수정 API",
        response_model=UserResponse,
)
def update_user_handler(
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_session),
):
        stmt = select(User).where(User.id == user_id)
        result = session.execute(stmt)
        user = result.scalar()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found",
            )
        
        user.job = body.job
        # session.add(user)
        session.commit() # job 상태(job 변경)를 db에 반영
            # e.g. UPDATE user SET job = '  ' WHERE user.id = 1;

# 회원 삭제 API
# DELETE//users/{user_id}
@router.delete(
        "/users/{user_id}",
        summary="회원 삭제 API",
        status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_handler(
    user_id: int,
    session = Depends(get_session),
):
# 1) get + delete
#   user 조회 후 삭제 
# 2) delete
#   delete 10 user -> 있으면 삭제, 없으면 무시
    
    # # 1) user 조회 후 삭제 
    # with SessionFactory() as session:
    #     stmt = select(User).where(User.id == user_id)
    #     result = session.execute(stmt)
    #     user = result.scalar()

    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="User Not Found",
    #         )
    
    #     session.delete(user) # 실제 객체(데이터)를 삭제
    #     # session.expunge(user) -> 세션의 추적대상에서 제거
    #     session.commit()

    # 2) 곧 바로 삭제
        stmt = delete(User).where(User.id == user_id)
        session.execute(stmt)
        session.commit()
    
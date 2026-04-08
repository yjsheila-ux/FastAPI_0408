from fastapi import APIRouter, Path, Query, status, HTTPException

from database.connection import SessionFactory
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse
# 강사님 코드 -> user 폴더 안으로 파일을 옮겼더니 바뀜.👍
# from request import UserCreateRequest
# from response import UserResponse

#user 핸들러 함수들을 관리하는 객체
router = APIRouter(tags=["User"])
                    #prefix="/users"
# 임시 데이터
users = [
        {"id": 1, "name": "alex", "job": "student"},
        {"id": 2, "name": "bob", "job": "sw engineer"},
        {"id": 3, "name": "chris", "job": "barista"},
    ]

@router.get("/users", status_code=status.HTTP_200_OK)
def get_users_handler():
    return users

# 사용자 정보 검색 API
# GET/ /users/search?name=alex
# GET/ /users/search?job=student
@router.get("/users/search")
def search_user_handler(
    name: str | None = Query(None),  # 타입힌트로 기본값을 none 으로 할당.
    job: str | None = Query(None),
):
    # 둘 다 아무것도 안보내는 경우
    if name is None and job is None:
        return{"msg":"조회에 사용할 QueryParam이 필요합니다."}
    return {"name":name, "job":job}


# 단일 사용자 API {user_id} 사용자 데이터 조회
@router.get("/users/{user_id}")
def get_user_handler(
    # ge =1 -> 1 이상 (= Greater then or Eual to ) 
    user_id: int = Path(..., ge=1), # le=9999, max_digits=6
    ):  #타입힌트로 숫자형으로 처리

    for user in users:
        if user["id"] == user_id:
            return user
        # return None 
# 존재하지 않는 유저는 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )

# 회원 가입(추가) API
# 메소드 = POST , 경로 = 메소드/users

@router.post(
        "/users",
        status_code=status.HTTP_201_CREATED,
        response_model=UserResponse,
)
def create_user_handler(
    # 1) 사용자 데이터를 받는다 + 데이터 유효성 검사
    body: UserCreateRequest
):
    # # 2) 사용자 데이터를 저장
    # new_user = {
    #     "id": len(users) + 1,
    #     "name": body.name,
    #     "job": body.job,
    #     "password": "password",
    # }
    # users.append(new_user)
    
        # # 3) 응답을 반환한다
    # # return {"name": body.name, "job": body.job}
    # # 1) return {"body": body}
    # return new_user 

    # session = SessionFactory()
    # context manager 를 벗어나는 순간 자동으로 close() 호출
    with SessionFactory() as session:
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
        response_model=UserResponse,
)
def update_user_handler(
    user_id: int,
    body: UserUpdateRequest,
):
    # 1) 클라이언트로부터 수정 할 데이터를 넘겨 받는다 (입력값)
    # 2) user_id로 사용자 조회, 데이터 수정(처리)
    for user in users:
        # 사용자 조회
        if user["id"] == user_id:
            # 데이터 수정
            user["job"] == body.job
            # 3) (반환)
            return user
    # 예외 처리
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )

# 회원 삭제 API
# DELETE//users/{user_id}
@router.delete(
        "/users/{user_id}",
        status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_handler(user_id: int):
    # 1) 입력
    # 2) 처리
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            # 3) 반환
            return # {"msg":"user delete..."} HTTP_204 에서 자체적으로 반환하지 않음.
    #예외 처리
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )
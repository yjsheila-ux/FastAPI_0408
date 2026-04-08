from fastapi import FastAPI, Path, Query, status, HTTPException
from user.request import UserCreateRequest
from user.response import UserResponse

# 127.0.0.1:8000 서버 실행
app = FastAPI()

# python 데코라이터 : 파이썬 함수에 추가적인 기능을 부여하는 문법
# @ -> python 

# GET / 요청이 들어오면 , root_handler 라는 함수를 시행.
@app.get("/", status_code=200)    # 성공 코드 status_code=200은 기본값이라 안써도 됨.
def root_handler():
    return{"ping": "pong"}

# GET / HELLO 요청이 들어오면  hello_handler 함수 시행.
@app.get("/hello", status_code=status.HTTP_200_OK)  # ("/ 경로")
def hello_handler():
    return{"message": "Hello FastAPI"}

# # # 전체 사용자 목록 조회 API
# # # GET / users
# # @app.get("/users")
# # def get_users_handler():
# #     return[
# #         {"id": 1, "name": "alex", "job": "student"},
# #         {"id": 2, "name": "bob", "job": "sw engineer"},
# #         {"id": 3, "name": "chris", "job": "barista"},
# #     ]

# # # 특정(단일) 사용자의 데이터 조회 API
# # # GET /usera/1 ->  1번 사용자 데이터 조회

# # @app.get("/users/1")
# # def get_user_one_handler():
# #     return {"id": 1, "name": "alex", "job": "student"}

# # # GET /usera/2 ->  2번 사용자 데이터 조회
# # @app.get("/users/2")
# # def get_user_two_handler():
# #     return {"id": 2, "name": "bob", "job": "sw engineer"}

# # # GET /usera/3 ->  3번 사용자 데이터 조회
# # @app.get("/users/3")
# # def get_user_three_handler():
# #     return {"id": 3, "name": "chris", "job": "barista"}

# # 변화하는 부분을 변수 처리
# # GET /usera/{user_id} ->  {user_id}번 사용자 데이터 조회

# # 임시 데이터
# users = [
#         {"id": 1, "name": "alex", "job": "student"},
#         {"id": 2, "name": "bob", "job": "sw engineer"},
#         {"id": 3, "name": "chris", "job": "barista"},
#     ]

# @app.get("/users", status_code=status.HTTP_200_OK)
# def get_users_handler():
#     return users

# # 사용자 정보 검색 API
# # GET/ /users/search?name=alex
# # GET/ /users/search?job=student
# @app.get("/users/search")
# def search_user_handler(
#     name: str | None = Query(None),  # 타입힌트로 기본값을 none 으로 할당.
#     job: str | None = Query(None),
# ):
#     # 둘 다 아무것도 안보내는 경우
#     if name is None and job is None:
#         return{"msg":"조회에 사용할 QueryParam이 필요합니다."}
#     return {"name":name, "job":job}

#     # for user in users:
#     #     if name and job. # and user["name"] == name and user["job"] == job:
#     #         if user["name"] == name and user["job"] == job:
#     #             return user
#     #         else:
#     #             return None
#     #     else:    
#     #         if user["name"] == name:
#     #             return user
#     #         if user["job"] == job:
#     #             return user
#     # # return None

# # 단일 사용자 API {user_id} 사용자 데이터 조회
# @app.get("/users/{user_id}")
# def get_user_handler(
#     # ge =1 -> 1 이상 (= Greater then or Eual to ) 
#     user_id: int = Path(..., ge=1), # le=9999, max_digits=6
#     ):  #타입힌트로 숫자형으로 처리
# #유저 아이디에 조건을 추가
#     # if user_id <= 0 :
#     #     raise ValueError("user_id는 양수여야 합니다.")
#     # if type(user_id) is not int:
#     #     raise ValueError("user_id 는 int 만 사용 가능합니다.")

#     for user in users:
#         if user["id"] == user_id:
#             return user
#         # return None 
# # 존재하지 않는 유저는 404
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="User Not Found",
#     )

# # Path vs Query
# # 데이터를 가져오는 위치가 다름.
# # Path 는 경로상에서 가져오기 때문에 경로 변수 필요 
# # Query 는 경로 변수 없음.


# # 회원 가입(추가) API
# # 메소드 = POST , 경로 = 메소드/users

# @app.post(
#         "/users",
#         status_code=status.HTTP_201_CREATED,
#         response_model=UserResponse,
# )
# def create_user_handler(
#     # 1) 사용자 데이터를 받는다 + 데이터 유효성 검사
#     body: UserCreateRequest
# ):
#     # 2) 사용자 데이터를 저장
#     new_user = {
#         "id": len(users) + 1,
#         "name": body.name,
#         "job": body.job,
#         "password": "password",
#     }
#     users.append(new_user)

#     # 3) 응답을 반환한다
#     # return {"name": body.name, "job": body.job}
#     # 1) return {"body": body}
#     return new_user # 3) 사용자가 아이디를 알 수 있음.
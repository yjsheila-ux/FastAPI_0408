# 요청 본문의 데이터 형식의 관리하는 파일
# 1)
from pydantic import BaseModel, Field

    # 데이터의 형식은  사용자 추가할 때, 클라이언트가 서버로 보내는 데이터 형식
class UserCreateRequest(BaseModel):
    # id: int  -> 생략, 식별자이므로 자동 생성하게 할것임.
    name: str = Field(..., min_length=2, max_length=10) #2글자 ~10글자
    job: str

# 클래스 -> 설계도, 요구조건  :타입힌트 로 사용 가능.

# 사용자 데이터를 수정할 때 데이터 형식
class UserUpdateRequest(BaseModel):
    job: str
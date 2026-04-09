# SQLAIchemy 를 이용해서 db와 연결하는 코드
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터 베이스 접속 정보
DATABASE_URL = "sqlite:///./local.db"

# ENGINE : db와 접속을 관리하는 객체
engine = create_engine(DATABASE_URL, echo=True)

# SESSION : 한 번의 db 요청-응답 단위 
SessionFactory = sessionmaker(
    bind=engine,
    # 데이터를 어떻게 다룰지를 조정하는 옵션
    autocommit = False,
    autoflush = False,
    expire_on_commit= False,
)

# session = SessionFactory()

# SQLALchemy 세션을 관리하는 함수 
def get_session():
    session = SessionFactory()
    try:
        yield session  # 일시정지
    finally:
        session.close()
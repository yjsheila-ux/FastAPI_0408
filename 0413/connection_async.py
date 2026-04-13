# SQLAIchemy 를 이용해서 db와 연결하는 코드
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# 데이터 베이스 접속 정보
DATABASE_URL = "sqlite+aiosqlite:///./local.db"

# ENGINE : db와 접속을 관리하는 객체
async_engine = create_engine(DATABASE_URL, echo=True)

# SESSION : 한 번의 db 요청-응답 단위 
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    # 데이터를 어떻게 다룰지를 조정하는 옵션
    autocommit = False,
    autoflush = False,
    expire_on_commit= False,
)

# session = SessionFactory()

# SQLALchemy 세션을 관리하는 함수 
async def get_async_session():
    session = AsyncSessionFactory()
    try:
        yield session  # 일시정지
    finally:
        await session.close()

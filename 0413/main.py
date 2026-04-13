import anyio
from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool

from fastapi import FastAPI
from user.router_1 import router

#쓰레드 풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

# # 동기 함수
# @app.get("/sync")
# def sync_handler():
#     import time
#     time.sleep(3)
#     return {"msg": "ok"}

# # 비동기라고 했는데 동기 쓰면 안됨.
# # 차라리 동기를 쓰면 
# # FastAPI 로 인해 비동기화 된다(스레드풀)
def aws_sync():
    # AWS 서버랑 통신 (예: 2초)
    return

@app.get("/async")
async def async_handler():
    # # 비동기 라이브러리를 지원하지 않는 경우
    # aws_sync() # time.sleep(2)

    # 동기 함수를 비동기 방식으로 실행 할 수 있게 해주는 유틸리티 함수 
    await run_in_threadpool(aws_sync)
    return {"msg": "ok"}

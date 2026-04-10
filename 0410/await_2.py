import asyncio
import time

# # 1) await 는 반드시 비동기 함수 안에서만 사용 가능하다.
# def hello():
#   ❌ await asyncio.sleep(2)

# 2) await 할 수 있는 코드 앞에서만 await를 쓸 수 있다.
async def hi():
    await time.sleep(2)

asyncio.run(hi())

#'NoneType' object can't be awaited
# time은 동기방식임. -> None 반환
# asyncio.sleep 으로 해야 비동식 방식임. -> 객체로 받을 수 있음.

#awaitable 
# 1. async def 
#   -> 호출하면 coroutine 객체를 반환해서 await 가능

async def hi():
    print("start hello..")
    await asyncio.sleep(2)
    print("end hello..")

async def main():
    print("start main..")
    coro = hi()
    await coro
    print("end main..")

asyncio.run(main())

# 2. 비 동기 라이브러리에서 온 함수인가? ()

# 3. I/O 대기 시간이 발생하는 작업인가? (DB, 네트워크, 파일, sleep)
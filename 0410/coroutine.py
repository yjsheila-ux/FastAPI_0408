# 동기식
# 1) 함수의 정의 : def foo(): 
# 2) 함수 호출(실행) : foo() => 함수 실행

# 비동기식
# 1) 코루틴 함수 (coroutine function) 정의 : asunc def boo():
# 2) 코루틴 호출 : boo() => 코루틴 객체를 생성
# 2-1) coro = boo() 객체를 변수에 저장
# 3) 코루틴 실행 

import asyncio

async def hello():
    print("hello")

# print(hello()) coro 객체를 보여주며 오류 발생

coro1 = hello()  # 객체 생성 후 변수 저장

asyncio.run(coro1) # 실행

# 실제 사용될땐 coro 가 많기때문에 묶어서 객체화 
# coro1 = hello()
# coro2 = hello()

# async def main():
#     await asyncio.gather(coro1, coro2)

# main_coro = main()
# asyncio.run(main_coro)
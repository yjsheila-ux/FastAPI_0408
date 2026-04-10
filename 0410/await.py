import time

# # 동기방식
# def a():
#     print("A 작업 시작")
#     time.sleep(2)   # I/O 작업처럼 대기 발생
#     print("A 작업 종료")

# def b():
#     print("B 작업 시작")
#     time.sleep(2)
#     print("B 작업 종료")

# start = time.time()
# a()
# b()
# end = time.time()
# print(f"실행 시간 : {end - start:.2f}")

import asyncio

# 비동기 
async def a():
    print("A 작업 시작")      # [1] a() 실행 시작
    await asyncio.sleep(2)  # [2] 2 초 대기 -> 양보  
    print("A 작업 종료")       # [5] a() 실행 종료

async def b():
    print("B 작업 시작")       # [3] b() 실행 시작
    await asyncio.sleep(2)   # [4] 2 초 대기 -> 양보  
    print("B 작업 종료")        # [6] b() 실행 종료
                            # 작업 속도가 빠르면 빠르게 종료 가능.
async def main():
    coro1 = a()
    coro2 = b()
    await asyncio.gather(coro1,coro2)

start = time.time()

asyncio.run(main())

end = time.time()

print(f"실행 시간 : {end - start:.2f}")





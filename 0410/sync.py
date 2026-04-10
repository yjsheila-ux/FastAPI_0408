# 동기(Syncronous)
# A 작업 -> B 작업

import time 

# 피호출자 (callee)
def hello():
    time.sleep(3)  #3초 대기 
    print("hello")
    #return None

hello() # 호출자(caller)
#coding=utf-8
'''
Created on 2016年10月14日

@author: pc
'''
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


def sayhello(n):
    time.sleep(1)
    print(10+n,"\n")
async def main():
    eonct=ThreadPoolExecutor(20)
    task=[]
    loop = asyncio.get_running_loop()
    for i in range(15):
        t=loop.run_in_executor(eonct,sayhello,i)
        task.append(t)
    await asyncio.wait(task)

if __name__ == "__main__":
    print(time.asctime(),"开始")
    asyncio.run(main())
    print(time.asctime(), "结束")






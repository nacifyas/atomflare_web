import asyncio
import time

async def task_search():
    print("begin search")
    await asyncio.sleep(1)
    print("end search")

async def task_fetch():
    print("begin fetch")
    await asyncio.sleep(2)
    print("end fetch")

async def task_query():
    print("begin query")
    await asyncio.sleep(4)
    print("end query")

async def main():
    g1 = await asyncio.gather(task_search(), task_fetch())
    # await asyncio.gather(task_query())
    



start_time = time.time()
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
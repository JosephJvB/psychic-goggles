from threading import Thread
import asyncio

async def prom(n):
  await asyncio.sleep(2)
  x = f'prom: {n}'
  print(x)
  return x

async def main():
  reqs = [prom(i) for i in range(3)]
  r = await asyncio.gather(*reqs)
  print('ee?', r)

asyncio.run(main())
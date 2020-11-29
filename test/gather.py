from threading import Thread
import asyncio

async def prom(n):
  await asyncio.sleep(2)
  x = f'prom: {n}'
  print(x)
  return x

async def main():
  r = await asyncio.gather(
    prom(1),
    prom(2),
  )
  print('ee?', r)

asyncio.run(main())
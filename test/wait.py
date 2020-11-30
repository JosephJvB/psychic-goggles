from threading import Thread
import asyncio

async def prom(n):
  await asyncio.sleep(2)
  x = f'prom: {n}'
  print(x)

def main():
  l = asyncio.get_event_loop()
  reqs = [prom(i) for i in range(3)]
  l.run_until_complete(asyncio.wait(reqs, return_when=asyncio.ALL_COMPLETED))
  print('done')

main()
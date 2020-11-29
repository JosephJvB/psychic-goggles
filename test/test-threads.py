# https://stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished

import time
from random import randrange
from threading import Thread

def promise(n):
  # s = randrange(1, 5)
  s = 2
  time.sleep(s)
  print('prom:', n, 'sleep:', s)
  return

pool = []
for i in range(4):
  t = Thread(target=promise, args=(i,))
  t.start()
  pool.append(t)

for t in pool:
  t.join()

print('done')
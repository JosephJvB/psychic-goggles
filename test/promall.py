import time
from random import randrange
from threading import Thread
from queue import Queue

def p1(n, q):
  s = 2
  time.sleep(s)
  x = f'prom: {n} sleep: {s}'
  print(x)
  q.put(x)

def pall(l):
  pool = []
  q = Queue()
  for i in l:
    t = Thread(target=p1, args=(i,q,))
    t.start()
    pool.append(t)

  for t in pool:
    t.join()

  print('done')
  for i in range(q.qsize()):
    print(q.get())


pall([1, 2, 3])
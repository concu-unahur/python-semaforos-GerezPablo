import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

sema = threading.Semaphore(3)
chefLock = threading.Lock()

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    
    chefLock.acquire()
    while (True):
      chefLock.acquire()
      try:
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      finally:
        sema.release()
        #chefLock.acquire()

        

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    
    sema.acquire()
    try:
      if(platosDisponibles > 0):
        platosDisponibles -= 1
        logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
      else:
        chefLock.release()
        sema.acquire()
    finally:
      sema.release()


platosDisponibles = 3

Cocinero().start()

for i in range(5):
  Comensal(i).start()


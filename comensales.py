import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

sema = threading.Semaphore(3)


class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    
    sema.acquire()
    while (True):
      logging.info('Reponiendo los platos...')
      platosDisponibles = 3
    sema.release()

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles

    sema.acquire()
    try:
      platosDisponibles -= 1
      logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
    finally:
      sema.release()

platosDisponibles = 3

Cocinero().start()

for i in range(5):
  Comensal(i).start()


from service import Service

class Menu:
  def __init__(self):
    self.service = Service()
  def run(self):
    print('==== Qatar World Cup ====')
    while True:
      m = input('MENU\n 1. Input Match Information\n 2. Exit\n')
      if m =='1':
        self.service.inputMatchInfo()
      elif m =='2':
        print('Exit Qatar World Cup')
        break
      else:
        print('Wrong Number')
if __name__ =='__main__':
  m = Menu()
  m.run()
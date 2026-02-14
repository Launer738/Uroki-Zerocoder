class Engine():

    def start(self):  # ← Добавьте self!
        print("Двигатель запущен")

    def stop(self):  # ← Добавьте self!
        print("Двигатель остановлен")

class Car():
    def __init__(self):
        self.engine = Engine()  # ← Исправьте опечатку: evgine → engine

    def start(self):
        self.engine.start()

    def stop(self):
        self.engine.stop()

my_car = Car()  # ← ВАЖНО: добавьте скобки () для создания объекта!
my_car.start()
my_car.stop()
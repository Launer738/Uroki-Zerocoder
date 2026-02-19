# ============================================
# ПЛАН ВЫПОЛНЕНИЯ ЗАДАЧИ: "БИТВА ГЕРОЕВ"
# ============================================
# 
# ЭТАП 1: СОЗДАНИЕ КЛАССА HERO
#   - Создать класс Hero
#   - Добавить атрибуты: name, health=100, attack_power=20
#   - Реализовать метод __init__(self, name) для инициализации
#   - Реализовать метод attack(self, other) для атаки другого героя
#   - Реализовать метод is_alive(self) для проверки жизни героя
#
# ЭТАП 2: СОЗДАНИЕ КЛАССА GAME
#   - Создать класс Game
#   - Добавить метод __init__(self) для создания игрока и компьютера
#   - Создать атрибуты: self.player и self.computer (экземпляры Hero)
#   - Реализовать метод start(self) с игровым циклом:
#     * Цикл while пока оба героя живы
#     * Игрок атакует компьютер
#     * Вывод информации об атаке и здоровье
#     * Компьютер атакует игрока
#     * Вывод информации об атаке и здоровье
#     * Проверка победителя и вывод результата
#
# ЭТАП 3: ЗАПУСК ИГРЫ
#   - Создать экземпляр игры: game = Game()
#   - Запустить игру: game.start()
#
# ============================================

class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 20

    def attack(self, other):
        other.health -= self.attack_power

    def is_alive(self):
        return self.health > 0

class Game:
    def __init__(self):
        self.player = Hero("Евгений")
        self.computer = Hero("Компьютер")

    def start(self):
        while self.player.is_alive() and self.computer.is_alive():
            self.player.attack(self.computer)
            print(f"{self.player.name} атакует {self.computer.name}")
            print(f"{self.computer.name} осталось {self.computer.health} здоровья")
            self.computer.attack(self.player)
            print(f"{self.computer.name} атакует {self.player.name}")
            print(f"{self.player.name} осталось {self.player.health} здоровья")
        if self.player.is_alive():
            print(f"{self.player.name} победил!")
        else:
            print(f"{self.computer.name} победил!")

# ============================================
game = Game()
game.start()








from abc import ABC, abstractmethod

class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

class Sword(Weapon):
    def attack(self):
        return "наносит удар мечом"

class Bow(Weapon):
    def attack(self):
        return "наносит удар из лука"

class Monster():
    def __init__(self, name, health):
        self.__name = name
        self.__health = health
    
    def get_name(self):
        return self.__name
    
    def get_health(self):
        return self.__health
    
    def take_damage(self, damage):
        self.__health -= damage
        if self.__health <= 0:
            self.__health = 0
    
    def is_alive(self):
        return self.__health > 0


class Fighter():
    def __init__(self, name):
        self.__name = name
        self.__weapon = None  # Пока оружия нет
    
    def get_name(self):
        return self.__name
    
    def change_weapon(self, weapon):
        self.__weapon = weapon
    
    def attack(self, monster):
        if self.__weapon is None:
            print(f"{self.__name} не имеет оружия!")
            return
        
        attack_description = self.__weapon.attack()
        print(f"{self.__name} {attack_description}")
        
        # Наносим урон монстру
        monster.take_damage(50)  # Например, 50 урона


# Создаем бойца
fighter = Fighter("Герой")

# Создаем монстра
monster = Monster("Орк", 100)

# Боец выбирает меч
sword = Sword()
fighter.change_weapon(sword)
print(f"{fighter.get_name()} выбирает меч.")
fighter.attack(monster)

# Проверяем результат
if not monster.is_alive():
    print(f"{monster.get_name()} побежден!")
else:
    print(f"{monster.get_name()} еще жив! Здоровье: {monster.get_health()}")

# Боец меняет оружие на лук
bow = Bow()
fighter.change_weapon(bow)
print(f"\n{fighter.get_name()} выбирает лук.")
fighter.attack(monster)

if not monster.is_alive():
    print(f"{monster.get_name()} побежден!")


class Axe(Weapon):  # Новое оружие - добавляем БЕЗ изменения существующего кода!
    def attack(self):
        return "наносит удар топором"

# Используем новое оружие
axe = Axe()
fighter.change_weapon(axe)
fighter.attack(monster)
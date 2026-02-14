class Animal():
    def __init__(self, name, age):
        self.__name = name
        self.__age = age    

    def make_sound(self):
        print("Животное издает звук")

    def eat(self):
      print(f"{self.__name} ест")


    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

# Создайте объект
my_animal = Animal("Барсик", 3)

# Вызовите методы
my_animal.make_sound()
my_animal.eat()
print(my_animal.get_name())

class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.__wing_span = wing_span

    def get_wing_span(self):
        return self.__wing_span

    def make_sound(self):
        print(f"{self.get_name()} чирикает: Чик-чирик!")

class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.__fur_color = fur_color

    def make_sound(self):
        print(f"{self.get_name()} издает звук: Мяу!")

    def get_fur_color(self):
        return self.__fur_color

class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.__scale_type = scale_type

    def make_sound(self):
        print(f"{self.get_name()} шипит: Шшшш!")

    def get_scale_type(self):
        return self.__scale_type

# Создайте объекты разных классов
bird1 = Bird("Воробей", 2, 15)
mammal1 = Mammal("Кот", 3, "рыжий")
reptile1 = Reptile("Змея", 1, "гладкая")

# Вызовите методы
bird1.make_sound()      # Выведет: Воробей чирикает: Чик-чирик!
mammal1.make_sound()   # Выведет: Кот издает звук: Мяу!
reptile1.make_sound()  # Выведет: Змея шипит: Шшшш!

# Проверьте наследование
bird1.eat()  # Метод eat() наследуется от Animal


def animal_sound(animals):
    for animal in animals: 
        animal.make_sound()

animals_list = [
    Bird("Воробей", 2, 15),      # Это Bird
    Mammal("Кот", 3, "рыжий"),   # Это Mammal
    Reptile("Змея", 1, "гладкая"), # Это Reptile
    Bird("Сова", 5, 80),         # Это Bird
    Mammal("Собака", 4, "черный") # Это Mammal
]

animal_sound(animals_list)

# ============================================
# КЛАСС Employee - базовый класс для сотрудников зоопарка
# ============================================
class Employee():
    def __init__(self, name, position):
        self.__name = name
        self.__position = position
    
    def get_name(self):
        return self.__name
    
    def get_position(self):
        return self.__position

# ============================================
# КЛАСС ZooKeeper - смотритель зоопарка (наследуется от Employee)
# ============================================
class ZooKeeper(Employee):
    def __init__(self, name):
        super().__init__(name, "смотритель")  # position всегда "смотритель"
    
    def feed_animal(self, animal):
        """Кормит животное"""
        print(f"{self.get_name()} кормит {animal.get_name()}")
        animal.eat()  # Вызываем метод eat() у животного

# ============================================
# КЛАСС Veterinarian - ветеринар (наследуется от Employee)
# ============================================
class Veterinarian(Employee):
    def __init__(self, name):
        super().__init__(name, "ветеринар")  # position всегда "ветеринар"
    
    def heal_animal(self, animal):
        """Лечит животное"""
        print(f"{self.get_name()} лечит {animal.get_name()}")
        print(f"{animal.get_name()} чувствует себя лучше!")

# ============================================
# КЛАСС Zoo - использует композицию
# ============================================
# Композиция: Zoo содержит списки животных и сотрудников
# ============================================
class Zoo():
    def __init__(self):
        self.__animals = []      # Список для хранения животных
        self.__employees = []    # Список для хранения сотрудников
    
    def add_animal(self, animal):
        """Добавляет животное в зоопарк"""
        self.__animals.append(animal)
    
    def add_employee(self, employee):
        """Добавляет сотрудника в зоопарк"""
        self.__employees.append(employee)
    
    def get_animals(self):
        """Возвращает список животных"""
        return self.__animals
    
    def get_employees(self):
        """Возвращает список сотрудников"""
        return self.__employees
    
    def show_info(self):
        """Выводит информацию о зоопарке"""
        print(f"\nВ зоопарке {len(self.__animals)} животных и {len(self.__employees)} сотрудников")
        print("\nЖивотные:")
        for animal in self.__animals:
            print(f"  - {animal.get_name()} ({type(animal).__name__})")
        print("\nСотрудники:")
        for employee in self.__employees:
            print(f"  - {employee.get_name()} ({employee.get_position()})")

# ============================================
# ТЕСТИРОВАНИЕ КЛАССА Zoo
# ============================================
# Создаем зоопарк
my_zoo = Zoo()

# Создаем животных
bird1 = Bird("Воробей", 2, 15)
bird2 = Bird("Сова", 5, 80)
mammal1 = Mammal("Кот", 3, "рыжий")
mammal2 = Mammal("Собака", 4, "черный")
reptile1 = Reptile("Змея", 1, "гладкая")

# Создаем сотрудников (используем новые классы)
keeper1 = ZooKeeper("Иван")      # Смотритель
vet1 = Veterinarian("Мария")     # Ветеринар
keeper2 = ZooKeeper("Петр")      # Еще один смотритель

# Добавляем животных в зоопарк
my_zoo.add_animal(bird1)
my_zoo.add_animal(bird2)
my_zoo.add_animal(mammal1)
my_zoo.add_animal(mammal2)
my_zoo.add_animal(reptile1)

# Добавляем сотрудников в зоопарк
my_zoo.add_employee(keeper1)
my_zoo.add_employee(vet1)
my_zoo.add_employee(keeper2)

# Выводим информацию о зоопарке
my_zoo.show_info()

# Демонстрируем специфические методы сотрудников
print("\n" + "="*50)
print("Работа сотрудников:")
print("="*50)
keeper1.feed_animal(bird1)      # Смотритель кормит животное
keeper2.feed_animal(mammal1)    # Другой смотритель кормит другое животное
vet1.heal_animal(reptile1)     # Ветеринар лечит животное

# Демонстрируем полиморфизм с животными из зоопарка
print("\n" + "="*50)
print("Звуки животных в зоопарке:")
print("="*50)
animal_sound(my_zoo.get_animals())
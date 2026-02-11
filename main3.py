class Bird():
    def __init__(self, name, voice, color):
        self.name = name
        self.voice = voice
        self.color = color

    def fly(self):
        print(f"{self.name} - летает")

    def eat(self):
        print(f"{self.name} - кушает")

    def sing(self):
        print(f"{self.name} поёт {self.voice}")

class pigeon(Bird):
    def __init__(self, name, voice, color, favorite_food):
        super().__init__(name, voice, color)
        self.favorite_food = favorite_food

    def food(self):
        print(f"{self.name} - любимая еда {self.favorite_food}")

bird1 = pigeon("Голубь", "волшебно", "синий", "жопа")
bird1.sing()
bird1.food()
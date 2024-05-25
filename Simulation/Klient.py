import random


class Klient:

    totalTime = 0
    def __init__(self, id : int):
        kolor = "black"
        self.exists = True
        self.family = random.randint(0, 5)
        self.id = id
        self.local = random.randint(0, 5)
        if self.local > 0:
            self.wroclaw = random.randint(0, 3)
        else:
            self.wroclaw = 0
        self.family = random.randint(0, 3)
        self.total = random.randint (10, 500) * self.family
        self.age = random.randint(10, 90)
        self.card = random.randint(0, 1)
        self.totalTime = random.randint(1, 2) + (self.family * 1) - self.card # oblicza calkowity czas na obsluge wliczajac wielkosc rodziny oraz posiadanie karty

    def getTotaltime(self):
        return self.totalTime

    def getId(self):
        return self.id

    def getFamily(self):
        return self.family
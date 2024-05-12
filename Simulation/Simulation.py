from numpy import random


def randomNumberGenerator(start, scl):
    # Generator losuje liczby od 1 do 10000 w celu symulacji prawdopodobienstwa
    # Poziom dokladnosci prawdopodobienstwa wynosi 0,01%
    # tzn aby wykonalo sie zdarzenie o prawdopodobienstwie 95,23%, musi wylosowac sie liczba 9532 lub mniejsza
    x = random.normal(loc= start, scale = scl)
    return x


def checkEvent(prob, rng):
    if rng < prob:
        print(rng)
        print("True")
        print(" ")
    else:
        print(rng)
        print("False")
        print(" ")


class Simulation:

    def __init__(self):
        probability = 5000
        #zdarzenie z 40%
        result = randomNumberGenerator(5000, 10)
        checkEvent(probability, result)



        # tymczasowa prezentacja dzialania symulatora

import random


def randomNumberGenerator():
    start = 1
    end = 10000
    # Generator losuje liczby od 1 do 10000 w celu symulacji prawdopodobienstwa
    # Poziom dokladnosci prawdopodobienstwa wynosi 0,01%
    # tzn aby wykonalo sie zdarzenie o prawdopodobienstwie 95,23%, musi wylosowac sie liczba 9532 lub mniejsza
    while True:
        yield random.randint(start, end)
    pass


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
        num_iteration = 10
        probability = 8000
        #zdarzenie z 80%
        rng = randomNumberGenerator()

        for _ in range(num_iteration):
            print("Wydarzenie:", _+1)
            checkEvent(probability, next(rng))

        # tymczasowa prezentacja dzialania symulatora

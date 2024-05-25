from numpy import random
import time

from Simulation.Kasa import Kasa
from Simulation.Klient import Klient
from Simulation.MyGui import MyGui


class Simulation:

    registries = []
    clients = []
    statsTotal = []
    statsDaily = []
    closingTime = False  #  okresla ostatnie 30 minut otwarcia sklepu
    rushHour = False

    maxTransactions = 50
    serviceTime = 5
    maxCapacity = 0

    #  wszelkie statystyki przeprowadzonego badania, ktore moga byc istotne
    #  staty totalne
    clientsTotal = 0
    clientsCard = 0
    clientsLocal = 0
    clientsWroclaw = 0
    familyTotal = 0
    cashTotal = 0
    avgAge = 0
    avgTime = 0

    #  statstyki godzinowe
    clientsTotalHour = 0
    clientsCardHour = 0
    clientsLocalHour = 0
    clientsWroclawHour = 0
    familyTotalHour = 0
    avgAgeHour = 0
    avgTimeHour = 0
    cashTotalHour = 0
    issues = 0
    queueOverflow = 0  # zlicza ilosc sytuacji, w ktorych kolejka zostala przepel

    clientsTotalDay = 0
    clientsCardDay = 0
    clientsLocalDay = 0
    clientsWroclawDay = 0
    familyTotalDay = 0
    cashTotalDay = 0
    avgAgeDay = 0
    avgTimeDay = 0

    def __init__(self, amount: int, days: int, hours: int, maxCapacity: int):
        self.start(amount, maxCapacity)
        self.gui = MyGui(amount, maxCapacity)
        self.theSimulation(days, hours)

    def addKasa(self, index: int, maxCapacity: int):
        self.registries.append(Kasa(index, maxCapacity))

    def start(self, amount: int, maxCap: int):
        self.maxCapacity = maxCap
        for x in range(amount):
           self.addKasa(x+1, maxCap)
        self.registries[0].active = True


    def theSimulation(self, days: int, hours: int):
        for dzien in range(days):

            for k in range(len(self.registries)):
                self.registries[k].resetQueue()

            self.gui.display_days(dzien % 7)

            self.openingTime = 8

            # zerowanie statystyk dniowych
            self.rushHour = False
            self.closingTime = False
            self.clientsTotalDay = 0
            self.clientsCardDay = 0
            self.clientsLocalDay = 0
            self.clientsWroclawDay = 0
            self.avgAgeDay = 0
            self.avgTimeDay = 0
            self.issues = 0
            self.queueOverflow = 0

            print(f"Dzien: {dzien}")
            for godzina in range(hours):
                print(f"Godzina: {self.openingTime + godzina}")
                # zerowanie statystyk godzinnych
                self.clientsCardHour = 0
                self.clientsTotalHour = 0
                self.clientsLocalHour = 0
                self.clientsWroclawHour = 0
                self.avgAgeHour = 0
                self.avgTimeHour = 0

                if godzina + self.openingTime == 12 or godzina + self.openingTime == 16:
                    self.rushHour = True
                elif godzina + self.openingTime == 14 or godzina + self.openingTime == 18:
                    self.rushHour = False

                for i in range(60):
                    print(f"Minuta : {i}")

                    for k in range(len(self.registries)):
                        if self.registries[k].getActive():
                            self.gui.kasa_change_color(k, "green")
                        else:
                            self.gui.kasa_change_color(k, "red")
                        if self.registries[k].getIncident():
                            self.gui.kasa_change_color(k, "gray")
                        if self.registries[k].getService():
                            self.gui.kasa_change_color(k, "orange")

                    self.gui.display_numbers((godzina + self.openingTime), i)

                    if hours - godzina == 1 and i == 30:
                        self.closingTime = True  # czas zamkniecia sklepu, nowi klienci nie przychodza

                    if not self.closingTime:
                        self.genClient(self.rushHour)

                    print(f"Ilosc nowych klientow: {len(self.clients)}")

                    j = 0  # zmienna konttrolna do dyspozycji klientow
                    # dyspozycja nowych klientow

                    while j < len(self.registries):
                        if self.registries[j].getActive():
                            break
                        else:
                            j += 1
                    if j == len(self.registries):
                        j = 0

                    while len(self.clients) > 0 and j < len(self.registries):
                        if j == len(self.registries) and len(self.clients) > 0:
                            break
                        if self.registries[j].addClient(self.clients[0]) == 1:
                            self.clients.pop(0)
                            j = 0
                        elif self.registries[j].addClient(self.clients[0]) == -7 and j < len(self.registries)-1:
                            j += 1
                        if not self.registries[j].getActive():
                            self.registries[j].setActive(True)


                    for k in range(len(self.registries)):
                        print(f"{len(self.registries[k].queue)}, zapelnienie kasy")

                    for k in range(len(self.registries)):
                        self.gui.klienci_change_color(k, self.registries[k].getQueuesize(), self.maxCapacity)
                    time.sleep(0.2)

                    if len(self.clients) != 0:
                        self.queueOverflow += 1

                    #  obsługa klienta

                    for k in range(len(self.registries)):
                        if self.registries[k].getDowntime() == 0 and self.registries[k].getIncident():
                            self.registries[k].resetDowntime()
                        elif self.registries[k].getDowntime() > 0:
                            self.registries[k].downtime = -1

                        if self.registries[k].getActive():  # sprawdzanie maksymalnej ilosci transakcji
                            if self.registries[k].getTotalTransaction == self.maxTransactions:
                                self.registries[k].close(self.clients)
                                self.registries[k].brokenStart(self.serviceTime)
                                print(f"Awaria kasy nr {k}")
                                self.issues += 1

                        self.registries[k].serveClient()
                        if self.registries[k].current == self.registries[k].temp:
                            #  sprawdza czy stoi temp - kasa jest pusta
                            if self.registries[k].cash >= 15000:
                                print(f"Kasa {k+1} pelna, przepraszamy")
                                self.registries[k].setDowntime(3)
                                self.registries[k].cash = 2000

                        if self.registries[k].getActive():
                            print(f"kasa", k+1, "stoi", self.registries[k].getIdle(), "minut pusta")
                        if self.registries[k].getIdle() == 5:
                            self.registries[k].close(self.clients)

                        if self.registries[k].getActive() and self.registries[k].getServing():
                            self.genIncident(self.registries[k])

                        if self.registries[k].getIncident():
                            self.registries[k].service -= 1
                            if self.registries[k].getService() == 0:
                                self.registries[k].brokenStop()
                                self.registries[k].open()

        self.showStats()

    def genClient(self, rush: bool):
        if rush:
            maxAmount = 8
            minAmount = 3
        else:
            maxAmount = 5
            minAmount = 0

        for client in range(random.randint(minAmount, maxAmount)):
            newClient = Klient(self.clientsTotal)
            self.clients.append(newClient)
            print(f"Wygenerowano klienta nr {newClient.id},z rodzina {newClient.family} czas obslugi wynosi {self.clients[client].totalTime}. ")
            self.clientsTotal += 1
            self.clientsTotalDay += 1
            self.clientsTotalHour += 1
            self.familyTotal += newClient.getFamily()
            self.familyTotalDay += newClient.getFamily()
            self.familyTotalHour += newClient.getFamily()
            self.cashTotal += newClient.total
            self.cashTotalDay += newClient.total
            self.cashTotalHour += newClient.total
            if newClient.card == 1:
                self.clientsCard += 1
                self.clientsCardHour += 1
                self.clientsCardDay += 1
            if newClient.wroclaw > 0:
                self.clientsWroclaw += 1
                self.clientsWroclawHour += 1
                self.clientsWroclawDay += 1
            if newClient.local > 0:
                self.clientsLocal += 1
                self.clientsLocalDay += 1
                self.clientsLocalHour += 1


    def showStats(self):
        print(f"Wszyscy klienci:{self.clientsTotal} ")
        print(f"Klienci placacy karta: {self.clientsCard}")
        print(f"Klienci placacy gotowka: {self.clientsTotal - self.clientsCard}")
        print(f"Klienci z Wrocławia: {self.clientsWroclaw}")
        print(f"Klieci spoza Wrocławia: {self.clientsTotal - self.clientsWroclaw}")
        print(f"Klienci polacy: {self.clientsLocal}")
        print(f"Klienci niepolacy: {self.clientsTotal - self.clientsLocal}")
        print(f"Koszt calkowity zakupow: {self.cashTotal} ")
        print(f"Ilosc rodziny z klientami: {self.familyTotal}")
        print(f"Ilosc awarii: {self.issues}")
        print(f"Ilosc przepelnien: {self.queueOverflow}")

    def genIncident(self, kasa: Kasa): # metoda generuje wypadek o prawdopod. 10% o dlugosci od 1 do 3 minut
        if random.randint(1, 50) == 5:
            kasa.setDowntime(random.randint(1, 3))
            print(f"AWARIA KASY", kasa.id)
            self.issues += 1

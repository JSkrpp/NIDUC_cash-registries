from Simulation.Klient import Klient


class Kasa:

    def __init__(self, id: int, maxCapacity: int):
        self.id = id
        self.serwis = 0
        self.incident = False
        self.downtime = 0
        self.active = False
        self.damaged = False
        self.totalTransaction = 0
        self.queue = []
        self.maxCapacity = maxCapacity
        self.temp = Klient # potrzeny do poprawnej implementacji dzialania kasy pustej ale otwartej
        self.temp.timeTotal = 0
        self.cash = 2000
        self.current = self.temp
        self.emptyTimer = 0
        self.serivng = False

    def getTotalTranscaction(self):
        return self.totalTransaction

    def getActive(self):
        return self.active

    def setActive(self, new: bool):
        self.active = new

    def getDowntime(self):
        return self.downtime

    def getServing(self):
        return self.serving
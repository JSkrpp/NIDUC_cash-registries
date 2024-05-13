from Simulation.Klient import Klient


class Kasa:

    def __init__(self, id: int, maxCapacity: int):
        self.id = id
        self.service = 0
        self.incident = False
        self.downtime = 0
        self.active = False
        self.broken = False
        self.totalTransaction = 0
        self.queue = []
        self.maxCapacity = maxCapacity
        self.temp = Klient # potrzeny do poprawnej implementacji dzialania kasy pustej ale otwartej
        self.temp.totalTime = 0
        self.cash = 2000
        self.current = self.temp
        self.idleTimer = 0
        self.serving = False

    def getTotalTranscaction(self):
        return self.totalTransaction

    def getActive(self):
        return self.active

    def setActive(self, new: bool):
        self.active = new

    def setIncident(self, new: bool):
        self.incident = new

    def getIncident(self):
        return self.incident
    def getDowntime(self):
        return self.downtime

    def getServing(self):
        return self.serving

    def setDowntime(self, time: int):
        self.setActive(False)
        self.setIncident(True)
        self.downtime += time

    def resetDowntime(self):
        self.setActive(True)
        self.setIncident(False)
        self.downtime = 0

    def getBroken(self):
        return self.broken

    def getQueue(self):
        return self.queue

    def getQueuesize(self):
        return len(self.queue)

    def getID(self):
        return self.id

    def getIdle(self):
        return self.idleTimer

    def addClient(self, klient: Klient):
        if self.getQueuesize() < self.maxCapacity:
            self.queue.append(klient)
            return 1
        else:
            return -7 # errorcode przepelnienia kasy

    def addCash(self, cash: int):
        if self.cash < 15000:
            self.cash += cash

    def brokenStart(self, serviceTime: int):
        self.broken = True
        self.service = serviceTime
        self.totalTransaction = 0

    def brokenStop(self):
        self.broken = False
        self.service = 0

    def open(self):
        self.active = True

    def close(self, kolejka):
        if len(self.queue) > 0:
            while len(self.queue) > 0:
                kolejka.append(self.queue.pop(0))
        self.active = False
        self.idleTimer = 0
    def serveClient(self):
        if not self.getActive(): return -7
        if self.current.totalTime == 0 and len(self.queue) > 0: # klient skonczyl obsluge, jest kolejka
            self.serving = True
            if len(self.queue) > 0:
                self.current = self.queue.pop(0)
                self.addCash(self.current.total)
                self.current.totalTime -= 1
                self.idleTimer = 0
        elif self.current.totalTime == 0:
            self.serving = False
            self.current = self.temp
            self.idleTimer += 1
        else:
            self.current.totalTime -= 1

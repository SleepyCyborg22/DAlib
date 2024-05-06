class Agent:
    vars = {}
    recMsg = {}
    sentMsg = {}
    enteredThrough = -1
    chosenPort = -1
    collocAgents = []
    currNodeDegree = 0

    def __init__(self, id, byzantine):
        self.id = id
        self.byzantine = byzantine
        pass

    def printInfo(self):
        print(self.enteredThrough, self.collocAgents, self.currNodeDegree)
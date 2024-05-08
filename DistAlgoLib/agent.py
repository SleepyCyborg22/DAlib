import random

def checkLowHigh(Arr, low, high, thresh):
    cnt = 0
    for a in Arr:
        if a < high and a >= low:
            cnt += 1

    return cnt >= thresh

def checkForward(msgs, thresh):
    cntTrue = 0
    cntFalse = 0
    for msg in msgs:
        temp = msgs[msg]
        if 'forward' in temp:
            if(temp['forward']):
                cntTrue+=1
            else:
                cntFalse += 1


    if (cntFalse < thresh and cntTrue < thresh):
        return False
    
    return cntTrue > cntFalse

def checkExchange(msgs, thresh, key):
    vals = {}
    for msg in msgs:
        temp = msgs[msg]
        if key in temp:
            temp2 = temp[key]
            if temp2 in vals:
                vals[temp2] += 1
            else:
                vals[temp2] = 1
    if not vals:
        return False
    
    (valMax, keyMax) = max(zip(vals.values(), vals.keys()))

    if valMax < thresh:
        return False

    return keyMax


class Agent:
    

    def __init__(self, id, byzantine):
        self.id = id
        self.byzantine = byzantine
        self.active = True
        self.vars = {}
        self.recMsg = {}
        self.sentMsg = {}
        self.collocAgents = []
        self.enteredThrough = -1
        self.chosenPort = -1
        self.currNodeDegree = 0
        self.active = True
        self.rounds = 0
        pass

    def printInfo(self):
        print(self.enteredThrough, self.collocAgents, self.currNodeDegree)

    def firstOperation(self):
        if not self.active:
            return

        if (self.rounds == 0):
            k = len(self.collocAgents)
            div = k//3
            group = 2
            self.vars["scout"] = False
            if self.id < div:
                group = 0
            elif self.id < 2*div:
                group = 1
                self.vars["scout"] = True
                
            minTrust = (div+2)//2
            self.vars["group"] = group
            self.vars["k"] = k
            self.vars["minTrust"] = minTrust
            self.vars["steps"] = 0
            self.vars["new"] = 0
            self.vars["forward"] = True
            self.vars["moving"] = True
            self.vars["exchange"] = False
            self.vars["infoComplete"] = False
            self.vars["finalTrav"] = False
            self.vars["exchangeComp"] = False

        if self.vars["finalTrav"]:
            return
        if self.vars["new"] >= 2*(self.vars["k"]//3) and not self.vars["exchangeComp"]:
            self.vars["exchange"] = True
        if self.vars["new"] >= self.vars["k"]:
            self.vars["infoComplete"] = True
        
        if self.vars["moving"]:
            if self.vars["forward"]:
                if self.id == self.vars["new"]:
                    print("-----------------",self.id, self.vars["steps"])
                    self.vars["stepsNeeded"] = self.vars["steps"]
                self.vars["new"] += 1

            self.vars["moving"] = False
            self.vars["forward"] = True

            if self.vars["new"] >= 2*(self.vars["k"]//3) and not self.vars["exchangeComp"]:
                self.vars["exchange"] = True
            if self.vars["new"] >= self.vars["k"]:
                self.vars["infoComplete"] = True

            return
        
        self.vars["g0"] = checkLowHigh(self.collocAgents, 0, self.vars["k"]//3, self.vars["minTrust"])
        self.vars["g1"] = checkLowHigh(self.collocAgents, self.vars["k"]//3, 2*(self.vars["k"]//3), self.vars["minTrust"])
        self.vars["g2"] = checkLowHigh(self.collocAgents, 2*(self.vars["k"]//3), self.vars["k"], self.vars["minTrust"])

        if self.vars["infoComplete"]:
            if (self.vars["g1"]):
                self.sentMsg["infoComplete"] = True
                self.vars["finalTrav"] = True
                self.vars["finalSteps"] = 0
            return

        if self.vars["exchange"] and self.vars["g2"] and self.vars["group"] == 0:
            self.vars["exchange"] = False
            self.sentMsg["enteredThrough"] = self.enteredThrough
            self.vars["moving"] = False
            self.vars["forward"] = True
            self.vars["exchangeComp"] = True
            return

        if self.vars["exchange"] and self.vars["g2"] and self.vars["group"] == 1:
            self.sentMsg["steps"] = self.vars["steps"]
            self.sentMsg["new"] = self.vars["new"]
            self.sentMsg["exchange"] = True
            self.vars["exchange"] = False
            self.vars["scout"] = False
            self.vars["exchangeComp"] = True
            return
        
        if self.vars["exchange"]:
            return


        if not self.vars["moving"] and self.vars["g0"] and self.vars["scout"]:
            self.sentMsg["forward"] = self.vars["forward"]
            self.vars["moving"] = True

        if not self.vars["moving"] and self.vars["scout"]:
            if (self.vars["group"] == 1 and self.vars["g2"]) or (self.vars["group"] == 2 and self.vars["g1"]):
                self.vars["forward"] = False
        

        if not self.vars["moving"] and self.vars["group"] == 0:
            if self.vars['g1'] and not self.vars["exchangeComp"]:
                self.vars["moving"] = True
            elif self.vars['g2'] and self.vars["exchangeComp"]:
                self.vars["moving"] = True

        return

    def secondOperation(self):
        if not self.active:
            self.rounds += 1
            self.sentMsg = {}
            self.chosenPort = -1
            return

        self.vars["g0"] = checkLowHigh(self.collocAgents, 0, self.vars["k"]//3, self.vars["minTrust"])
        self.vars["g1"] = checkLowHigh(self.collocAgents, self.vars["k"]//3, 2*(self.vars["k"]//3), self.vars["minTrust"])
        self.vars["g2"] = checkLowHigh(self.collocAgents, 2*(self.vars["k"]//3), self.vars["k"], self.vars["minTrust"])

        if self.vars["finalTrav"]:
            if self.vars["finalSteps"] == self.vars["stepsNeeded"]:
                self.active = False
                self.chosenPort = -1
            elif self.vars["finalSteps"] == 0:
                self.chosenPort = 0
            else:
                self.chosenPort = (self.enteredThrough + 1)%self.currNodeDegree
            self.vars["finalSteps"] += 1
        elif self.vars["infoComplete"]:
            self.chosenPort = (self.enteredThrough + 1)%self.currNodeDegree
        else:
            if self.vars["exchange"] and self.vars["g0"] and self.vars["group"] == 2:
                self.vars["exchange"] = False
                self.enteredThrough = checkExchange(self.recMsg, self.vars["minTrust"], 'enteredThrough')
                self.vars["moving"] = False
                self.vars["forward"] = True
                self.vars["exchangeComp"] = True

            if self.vars["group"] == 0:
                if self.vars["moving"]:
                    self.chosenPort = (self.enteredThrough + 1)%self.currNodeDegree
                    self.vars["steps"] += 1
                    self.vars["forward"] = checkForward(self.recMsg, self.vars["minTrust"])
                else:
                    self.chosenPort = -1
            else:
                if self.vars["scout"]:
                    if self.vars["moving"]:
                        self.chosenPort = self.enteredThrough
                        if self.chosenPort == -1:
                            self.chosenPort = 0
                        self.vars["steps"] += 1
                    else:
                        self.chosenPort = (self.enteredThrough + 1)%self.currNodeDegree
                else:
                    if self.vars['g1'] and self.vars['group'] == 2:
                        exch = checkExchange(self.recMsg, self.vars['minTrust'], 'exchange')
                        if not exch:
                            self.chosenPort = -1
                        else:
                            self.vars['exchange'] = True
                            self.vars['scout'] = True
                            self.vars['steps'] = checkExchange(self.recMsg, self.vars['minTrust'], 'steps')
                            self.vars['new'] = checkExchange(self.recMsg, self.vars['minTrust'], 'new')
                    elif self.vars['group'] == 1 and not self.vars['scout']:
                        finale = checkExchange(self.recMsg, self.vars['minTrust'], 'infoComplete')
                        if not finale:
                            self.chosenPort = -1
                        else:
                            self.vars["infoComplete"] = True
                            self.vars["finalSteps"] = 1
                            self.vars["finalTrav"] = True
                            self.chosenPort = 0
                    else:
                        self.chosenPort = -1

        self.rounds += 1
        self.sentMsg = {}

        return
    
    def byzantineOperation(self):
        deg = self.currNodeDegree
        chosenPortNum = random.randint(0, deg)
        if (chosenPortNum == deg):
            chosenPortNum = -1
        self.chosenPort = chosenPortNum
        return self
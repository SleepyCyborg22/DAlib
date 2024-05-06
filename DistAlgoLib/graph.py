import node
import agent
import random
from heapq import heapify, heappush, heappop 

class Graph:
    nodes = []
    agents = []

    def __init__(self, n) -> None:
        self.n = n
        for i in range(n):
            tempNode = node.Node()
            self.nodes.append(tempNode)
        pass

    def CreateRandomTree(self):
        adjList = []
        cnt = []
        for i in range(self.n):
            adjList.append([])
            cnt.append(0)

        pruferSequence = []

        for i in range(self.n - 2) :
            pruferSequence.append(random.randint(0, self.n-1))
            # print(pruferSequence[i])
            cnt[pruferSequence[i]] += 1

        heap = []
        heapify(heap)

        for i in range(self.n):
            if (cnt[i] == 0) :
                heappush(heap, i)

        for i in range(self.n - 2):
            x = pruferSequence[i]
            y = heappop(heap)
            adjList[x].append(y)
            adjList[y].append(x)
            cnt[x] -= 1
            if (cnt[x] == 0) :
                heappush(heap, x)

        z = heappop(heap)
        adjList[self.n-1].append(z)
        adjList[z].append(self.n-1)

        # print(adjList)

        for i in range(self.n):
            self.nodes[i].edges = adjList[i]

        return
    
    def InitializeGatheredConfiguration(self, k, byz):
        root = random.randint(0, self.n - 1)

        byzantine = [0] * k
        while (byz > 0) :
            i = random.randint(0, k-1)
            if (byzantine[i] == 0) :
                byzantine[i] = 1
                byz -= 1

        temp = []
        for i in range(k):
            tempAgent = agent.Agent(i, byzantine[i] == 1)
            self.agents.append(tempAgent)
            temp.append(i)

        self.nodes[root].agents = temp

        return
    

    def roundStartInformation(self):
        for i in range(self.n):
            deg = len(self.nodes[i].edges)
            agentsOnNode = self.nodes[i].agents
            print(i, agentsOnNode)
            for j in range(len(agentsOnNode)):
                self.agents[agentsOnNode[j]].currNodeDegree = deg
                self.agents[agentsOnNode[j]].collocAgents = agentsOnNode
        return
    
    def communication(self):
        for i in range(self.n):
            msg = {}
            agentsArr = self.nodes[i].agents
            for j in range(len(agentsArr)):
                currAgent = self.agents[agentsArr[j]]
                msg[str(currAgent.id)] = currAgent.sentMsg
            for j in range(len(agentsArr)):
                self.agents[agentsArr[j]].recMsg = msg
        return

    def nxtRound(self):
        nxtNodes = []
        for i in range(self.n):
            nxtNodes.append([])
        for i in range(self.n):
            agentsArr = self.nodes[i].agents
            for j in range(len(agentsArr)):
                nxt = self.agents[agentsArr[j]].chosenPort
                if (nxt == -1) :
                    nxtNodes[i].append(agentsArr[j])
                else:
                    temp = self.nodes[i].edges[nxt]
                    nxtNodes[temp].append(agentsArr[j])
                    for k in range(len(self.nodes[temp].edges)):
                        if (self.nodes[temp].edges[k] == i):
                            self.agents[agentsArr[j]].enteredThrough = k
                            break
        
        for i in range(self.n):
            self.nodes[i].agents = nxtNodes[i]

        return
import graph
import random

G = graph.Graph(15)

G.CreateRandomTree()

G.InitializeGatheredConfiguration(15,2)

for rnds in range(100):
    G.roundStartInformation()

    # for i in range(len(G.agents)):
    #     G.agents[i].printInfo()

    for i in range(len(G.agents)):
        temp = {}
        temp["A"] = random.randint(0,12)
        G.agents[i].sentMsg = temp

    G.communication()
    # for i in range(len(G.agents)):
    #     print(G.agents[i].sentMsg, G.agents[i].recMsg)

    for i in range(len(G.agents)):
        deg = G.agents[i].currNodeDegree
        chosenPortNum = random.randint(0, deg)
        if (chosenPortNum == deg):
            chosenPortNum = -1
        G.agents[i].chosenPort = chosenPortNum

    G.nxtRound()

    print('--------------------------------------------------------------------')
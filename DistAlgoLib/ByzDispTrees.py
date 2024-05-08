import graph
import networkx as nx
import matplotlib.pyplot as plt

numNodes = 6
numAgents  = 6
numByzantine = 0

def ByzDispTree(numNodes, numAgents, numByzantine):
    G = graph.Graph(numNodes)
    G.CreateRandomTree()

    G.InitializeGatheredConfiguration(numAgents, numByzantine)

    plotG = nx.Graph()
    for i in range(G.n):
        plotG.add_node(i)

    for i in range(G.n):
        for j in range(len(G.nodes[i].edges)):
            plotG.add_edge(i, G.nodes[i].edges[j])

    labeldict = {}
    for i in range(G.n):
        labeldict[i] = ', '.join(str(x) for x in G.nodes[i].agents)

    nx.draw_networkx(plotG, labels=labeldict)
    plt.show()

    numRounds = 0

    while True:
        numRounds += 1
        G.roundStartInformation()

        for i in range(len(G.agents)):
            if not G.agents[i].byzantine:
                G.agents[i].firstOperation()

            else:
                G.agents[i].byzantineOperation()

        G.communication()

        for i in range(len(G.agents)):
            if not G.agents[i].byzantine:
                G.agents[i].secondOperation()
            else:
                G.agents[i].byzantineOperation()

        G.nxtRound()

        if G.isDispersed() :
            break
        
        if numRounds%5 == 0:
            labeldict = {}
            for i in range(G.n):
                labeldict[i] = ', '.join(str(x) for x in G.nodes[i].agents)

            nx.draw_networkx(plotG, labels=labeldict)
            plt.show()

        print(numRounds, "-------------------------------")

    for i in range(len(G.agents)):
        print(G.agents[i].active, G.agents[i].vars)

    labeldict = {}
    for i in range(G.n):
        labeldict[i] = ', '.join(str(x) for x in G.nodes[i].agents)

    nx.draw_networkx(plotG, labels=labeldict)
    plt.show()

    if G.isDispersed():
        print("Accomplished")
    return numRounds


# ByzDispTree(numNodes, numAgents, numByzantine)
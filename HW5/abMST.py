"""
file: abMST.py
description: CSCI-665.04 - HMWK5: Q4 Subsequence with greatest sum
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779

Graph code are referred from the course CSCI 603
"""

import sys
class Vertex:

    __slots__ = 'id', 'connectedTo', 'group'

    def __init__(self, key):
        """
        Initialize
        """
        self.id = key
        self.connectedTo = {}
        self.group = ''

    def addNeighbor(self, nbr, weight=0):

        self.connectedTo[nbr] = weight

    def __repr__(self):
        return f"{str(self.id)}"  # + ' connectedTo: ' + str([str(x.id) for x in self.connectedTo])

    def __str__(self):
        return str(self.id) + ' | group: ' + self.group + ' | connectedTo: ' + str(
            [str(x.id) for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    __slots__ = 'vertList', 'numVertices'

    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        # count this vertex if not already present
        if self.getVertex(key) == None:
            self.numVertices += 1
            vertex = Vertex(key)
            self.vertList[key] = vertex
        return vertex

    def getVertex(self, key):
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None

    def __contains__(self, key):

        return key in self.vertList

    def addEdge(self, src, dest, cost=0):

        if src not in self.vertList:
            self.addVertex(src)
        if dest not in self.vertList:
            self.addVertex(dest)
        self.vertList[src].addNeighbor(self.vertList[dest], cost)

    def getVertices(self):

        return self.vertList.keys()

    def __iter__(self):

        return iter(self.vertList.values())

    def dfsCC(self, vertex, visited, cc):
        visited.append(vertex)
        BaseVertex = self.getVertex(vertex)
        cc.append(vertex)

        for neighbour in BaseVertex.getConnections():
            if neighbour.id not in visited:
                visited.append(neighbour.id)
                cc = self.dfsCC(neighbour.id, visited, cc)
        return cc

    def connectedComponents(self):
        visited = []
        connectedComponents = []
        for vertex in self.getVertices():
            if vertex not in visited:
                connectedComponents.append(self.dfsCC(vertex, visited, []))

        return connectedComponents

"""
  Gets input from user and creates the graph structure
"""
def createBaseGraph():
    n = int(input())
    m = int(input())
    group = []
    for i in range(n):
        group.append(int(input()))

    mainGraph = Graph()
    connections = []
    groupA = Graph()
    groupB = Graph()

    for i in range(m):
        edge = [int(i) for i in input().split()]
        vert1=edge[0]
        vert2=edge[1]
        weight=edge[2]

        #For bidirectional graph
        mainGraph.addEdge(vert1, vert2, weight)
        mainGraph.addEdge(vert2, vert1, weight)

        if group[vert1] == 0 and group[vert2] == 0:
            groupA.addEdge(vert1, vert2,weight)
            groupA.addEdge(vert2, vert1, weight)
        elif group[int(edge[0])] == 1 and group[int(edge[1])] == 1:
            groupB.addEdge(vert1, vert2,weight)
            groupB.addEdge(vert2, vert1, weight)
        else:
            connections.append((vert1, vert2, weight))

    return groupA, groupB, mainGraph, connections


def createGraphFromWCC(graph,wccs):
    """
    Creates graph from each weakly connected component
    """
    listOfGraphs = []
    for wc in wccs:
        inProcess = Graph()
        for vertexID in wc:
            vertex = graph.getVertex(vertexID)
            for neighbour in vertex.getConnections():
                edgeCost=vertex.getWeight(neighbour)
                if neighbour.id in wc:
                    inProcess.addEdge(vertexID, neighbour.id, edgeCost)
                    inProcess.addEdge(neighbour.id, vertexID, edgeCost)
        listOfGraphs.append(inProcess)
    return listOfGraphs


def getMST(baseGraph,graph, SCC):
    """
    Gets MST for given graph
    """
    def update(vertex: Vertex, seen):
        for neighbour in vertex.getConnections():
            if neighbour.id in seen:
                continue
            if cost[neighbour.id] > vertex.getWeight(graph.getVertex(neighbour.id)):
                cost[neighbour.id] = vertex.getWeight(graph.getVertex(neighbour.id))
                parent[neighbour.id] = vertex.id

    MST = []
    cost = [float("inf") for _ in range(len(baseGraph.vertList))]
    parent = [None for _ in range(len(baseGraph.vertList))]
    begin = SCC.pop()
    seen = []
    seen.append(begin)
    update(graph.getVertex(begin), seen)
    for i in range(len(SCC)):
        minVertex = cost.index(min(cost))
        MST.append(
            (minVertex, parent[minVertex], graph.getVertex(minVertex).getWeight(graph.getVertex(parent[minVertex]))))
        update(graph.getVertex(minVertex), seen)
        seen.append(minVertex)
        cost[minVertex] = float('inf')
    return MST


def getCombinedWeight(sortedMST, sortedCrossings):
    """
    Calculates the final weight
     """
    MSTW = 0
    for edge in sortedMST:
        MSTW += edge[2]

    finalWeight = sortedCrossings[0][2] + MSTW

    maxMSTEdge = sortedMST[0]
    for edge in sortedCrossings[1:]:
        if maxMSTEdge[0] == edge[0] or maxMSTEdge[0] == edge[1] or maxMSTEdge[1] == edge[0] or maxMSTEdge[1] == edge[1]:
            if edge[2] < maxMSTEdge[2]:
                finalWeight -= maxMSTEdge[2]
                finalWeight += edge[2]
                return finalWeight
            else:
                continue
    return finalWeight

def checkIfGroupsAreConnected(graph,wcc):
    """
    Check if grups are connected
    """
    for vertexID in wcc:
        vertex = graph.getVertex(vertexID)
        for neighbour in vertex.getConnections():
            if neighbour.id not in wcc:
                return True
    return False





if __name__ == '__main__':
    groupA, groupB, BaseGraph, crossings = createBaseGraph()

    groupA_CC = groupA.connectedComponents()
    groupB_CC = groupB.connectedComponents()
    totalSCC = groupA_CC + groupB_CC

    if len(totalSCC) >= 4:
        print(-1)
        sys.exit()

    if len(crossings) == 0:
        print(-1)
        sys.exit()


    groupsNotConnected = False
    for scc in totalSCC:
        if checkIfGroupsAreConnected(BaseGraph,scc) == False:
            groupsNotConnected = True

    if groupsNotConnected == True:
        print(-1)
        sys.exit()



    gACCGraphs = createGraphFromWCC(BaseGraph,groupA_CC)
    gBCCGraphs = createGraphFromWCC(BaseGraph,groupB_CC)



    msts = []

    for i in range(len(groupA_CC)):
        msts.extend(getMST(BaseGraph,gACCGraphs[i], groupA_CC[i]))

    for i in range(len(groupB_CC)):
        msts.extend(getMST(BaseGraph,gBCCGraphs[i], groupB_CC[i]))


    sortedMST = sorted(msts, key=lambda x: x[2], reverse=True)
    sortedCrossings = sorted(crossings, key=lambda x: x[2], reverse=False)

    if len(totalSCC)==3:
        if len(groupA_CC)==2:
            groupToConsider=groupA_CC
        else:
            groupToConsider = groupB_CC

        g1_crossings=[]
        g2_crossings=[]
        g1=groupA_CC[0]
        for crossings in sortedCrossings:
            if crossings[0] in g1 or crossings[1] in g1:
                g1_crossings.append(crossings)
            elif crossings[0] not in g1 or crossings[1] not in g1:
                g2_crossings.append(crossings)

        MSTW = 0
        for edge in sortedMST:
            MSTW += edge[2]
        mstTotal=MSTW

        print(mstTotal + g1_crossings[0][2] + g2_crossings[0][2])
        sys.exit()


    print(getCombinedWeight(sortedMST, sortedCrossings))

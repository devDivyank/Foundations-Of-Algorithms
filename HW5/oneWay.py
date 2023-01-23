"""
file: oneWay.py
description: CSCI-665.04 - HMWK5: Q3 Determine if there exists a pair of vertices u and v such
                                    that adding an edge from u to v makes the graph strongly connected
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779
"""

import sys
sys.setrecursionlimit(10**6)

class ClusterVertex():
    '''
    class to store a strongly connected component of the graph as one vertex of the macro graph
    '''
    def __init__(self, SCC: list, neighbours: list):
        """
            constructor for clusterVertex object

            :param SCC: a list of all SCCs in the graph
            :param neighbours: neighbours/edges in original graph as adjacency list
        """
        self.vertices = SCC
        self.neighbours = []
        self.incoming = 0
        self.outgoing = 0
        # counting the outgoing edges for the macro vertex
        for vertex in SCC:
            for neighbour in neighbours[vertex]:
                if neighbour not in SCC:
                    self.neighbours.append(neighbour)
                    if self.outgoing == 0:
                        self.outgoing += 1

    def __repr__(self):
        return str((self.vertices, self.neighbours, self.incoming, self.outgoing))

def finishOrderDFS(vertices, neighbours):
    """
        find the finishing times of vertices for a DFS traversal

        :param vertices: a list of all vertices in the graph
        :param neighbours: neighbours/edges in original graph as adjacency list
        :return: finishing times for each vertex in a list where index is the vertex
    """
    def DFS(vertex, neighbours, seen, finishTimes, time):
        seen[vertex] = True
        for neighbour in neighbours[vertex]:
            if not seen[neighbour]:
                time = DFS(neighbour, neighbours, seen, finishTimes, time)
        time += 1
        finishTimes[vertex] = time
        return time

    seen = [False] * len(vertices)
    finishTimes = [float("inf")] * len(vertices)
    time = 0
    for vertex in vertices[1:]:
        if not seen[vertex]:
            time = DFS(vertex, neighbours, seen, finishTimes, time)
    return finishTimes

def invertNeighbours(neighbours : list):
    """
        reversed edges of a graph by flipping the neighbours in adjacency list

        :param neighbours: neighbours of original graph as adjacency list
        :return: adjacency matrix for the reversed graph
    """
    invertedNeighbours = [[] for _ in range(len(neighbours))]
    for neighbour in neighbours[1:]:
        for n in neighbour:
            invertedNeighbours[n].append(neighbours.index(neighbour))
    return invertedNeighbours

def getSCC(vertex, neighbours, seen, currentSCC):
    """
        DFS traversal to obtain the strongly connected component the starting
        vertex belongs to

        :param vertex: starting vertex for DFS traversal
        :param neighbours: neighbours/edges in original graph as adjacency list
        :param seen: vertices already seen this current DFS iteration
        :param currentSCC: vertices already found to be in the current strongly connected component
        :return: vertices in the strongly connected component, in a list
    """
    seen[vertex] = True
    for neighbour in neighbours[vertex]:
        if not seen[neighbour]:
            currentSCC.append(neighbour)
            return getSCC(neighbour, neighbours, seen, currentSCC)
    return currentSCC

def findAllSCC(vertices, neighbours):
    """
        DFS traversal to obtain all the strongly connected components in the graph

        :param vertices: all the vertices in the original graph
        :param neighbours: neighbours/edges in original graph as adjacency list
        :return: all the strongly connected component in the graph, in a list
    """
    allSCC = []
    finishTimes = finishOrderDFS(vertices, neighbours)
    vertexOrder = vertexInOrder(finishTimes)[1:]
    inverseNeighbours = invertNeighbours(neighbours)
    seen = [False] * len(vertices)
    while vertexOrder:
        vertex = vertexOrder.pop()
        currentSCC = [vertex]
        if not seen[vertex]:
            currentSCC = getSCC(vertex, inverseNeighbours, seen, currentSCC)
            allSCC.append(currentSCC)
    return allSCC

def getMacroVertices(allSCC, neighbours):
    """
        function to obtain a list of vertices in macro graph using the SCCs found
        in the original graph

        :param allSCC: all the strongly connected component in the graph, in a list
        :param neighbours: neighbours/edges in original graph as adjacency list
        :return: a list of clusterVertex objects, each representing a vertex in the macro graph
    """
    macroVertices = [-1]
    for cluster in allSCC:
        macroVertices.append(ClusterVertex(cluster, neighbours))
    return macroVertices

def getClusterMapping(vertices, allSCC):
    """
        returns a list which maps each vertex in original graph to the vertex it belongs to in macro graph

        :param vertices: all the vertices in the original graph
        :param allSCC: all the strongly connected component in the graph, in a list
        :return: a list of clusterVertex objects, each representing a vertex in the macro graph
    """
    clusterArray = [-1] * len(vertices)
    for i in range(len(allSCC)):
        for vertex in allSCC[i]:
            clusterArray[vertex] = i + 1
    return clusterArray

def findIncoming(macroVertices, clusterMapping):
    """
        finds the incoming edges for each clusterVertex in the macro graph

        :param macroVertices: all the vertices in the macro graph
        :param clusterMapping: mapping of each vertex in original graph with clusterVertex it belongs to in macro graph
    """
    for cluster in macroVertices[1:]:
        for neighbour in cluster.neighbours:
            if macroVertices[clusterMapping[neighbour]].incoming == 0:
                macroVertices[clusterMapping[neighbour]].incoming += 1

def getMinEdges(macroVertices):
    """
        returns the minimum number of edges needed to be added to make the whole graph strongly connected

        :param macroVertices: all the vertices in the macro graph
        :return: the extra edges required
    """
    totalIn = 0
    totalOut = 0
    N = len(macroVertices) - 1
    for clusterVertex in macroVertices[1:]:
        totalIn += clusterVertex.incoming
        totalOut += clusterVertex.outgoing
    return max(N - totalIn, N - totalOut)

def vertexInOrder(finishTimes):
    """
        sorts the vertices in the order of decreasing finish times in DFS traversals

        :param finishTimes: finish times of all the vertices
        :return: list or ordered vertices
    """
    vertexOrder = finishTimes.copy()
    for x, id in zip(finishTimes, range(len(finishTimes))):
        if x == float('inf'):
            continue
        vertexOrder[x] = id
    return vertexOrder

if __name__ == '__main__':
    n = int(input())
    neighbours = [[]]
    vertices = [-1]

    # storing the edges as adjacency list 'neighbours'
    for i in range(1, n+1):
        neighbour = [int(i) for i in input().split()[:-1]]
        vertices.append(i)
        neighbours.append(neighbour)
    # find all the SCCs in the graph
    allSCC = findAllSCC(vertices, neighbours)

    # finding the incoming and outgoing edges for each vertex in macro graph
    clusterMapping = getClusterMapping(vertices, allSCC)
    macroVertices = getMacroVertices(allSCC, neighbours)
    findIncoming(macroVertices, clusterMapping)

    # if only 1 edge if needed to make the graph strongly conneceted, we print 'YES'
    if getMinEdges(macroVertices) == 1:
        print("YES")
    else:
        print("NO")



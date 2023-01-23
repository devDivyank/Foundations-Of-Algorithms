"""
file: morale.py
description: CSCI-665.04 - HMWK6: Q1 determine the number of employees at risk of spiralling endlessly
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779

Implementation for Graph and Vertex from: CSCI-620 - Computational Problem Solving
"""

class Vertex:
    """
    An individual vertex in the graph.

    :slots: id:  The identifier for this vertex (user defined, typically
        a string)
    :slots: connectedTo:  A dictionary of adjacent neighbors, where the key is
        the neighbor (Vertex), and the value is the edge cost (int)
    """

    __slots__ = 'id', 'connectedTo'

    def __init__(self, key):
        """
        Initialize a vertex
        :param key: The identifier for this vertex
        :return: None
        """
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        """
        Connect this vertex to a neighbor with a given weight (default is 0).
        :param nbr (Vertex): The neighbor vertex
        :param weight (int): The edge cost
        :return: None
        """
        self.connectedTo[nbr] = weight

    def __str__(self):
        """
        Return a string representation of the vertex and its direct neighbors:

            vertex-id connectedTo [neighbor-1-id, neighbor-2-id, ...]

        :return: The string
        """
        return str(self.id) + ' connectedTo: ' + str([str(x.id) for x in self.connectedTo])

    def getConnections(self):
        """
        Get the neighbor vertices.
        :return: A list of Vertex neighbors
        """
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        """
        Get the edge cost to a neighbor.
        :param nbr (Vertex): The neighbor vertex
        :return: The weight (int)
        """
        return self.connectedTo[nbr]

class Graph:
    """
    A graph implemented as an adjacency list of vertices.

    :slot: vertList (dict):  A dictionary that maps a vertex key to a Vertex
        object
    :slot: numVertices (int):  The total number of vertices in the graph
    """

    __slots__ = 'vertList', 'numVertices'

    def __init__(self):
        """
        Initialize the graph
        :return: None
        """
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        """
        Add a new vertex to the graph.
        :param key: The identifier for the vertex (typically a string)
        :return: Vertex
        """
        # count this vertex if not already present
        if self.getVertex(key) == None:
            self.numVertices += 1
            vertex = Vertex(key)
            self.vertList[key] = vertex
        return vertex

    def getVertex(self, key):
        """
        Retrieve the vertex from the graph.
        :param key: The vertex identifier
        :return: Vertex if it is present, otherwise None
        """
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None

    def __contains__(self, key):
        """
        Returns whether the vertex is in the graph or not.  This allows the
        user to do:

            key in graph

        :param key: The vertex identifier
        :return: True if the vertex is present, and False if not
        """
        return key in self.vertList

    def addEdge(self, src, dest, cost=0):
        """
        Add a new directed edge from a source to a destination of an edge cost.
        :param src: The source vertex identifier
        :param dest: The destination vertex identifier
        :param cost: The edge cost (defaults to 0)
        :return: None
        """
        if src not in self.vertList:
            self.addVertex(src)
        if dest not in self.vertList:
            self.addVertex(dest)
        self.vertList[src].addNeighbor(self.vertList[dest], cost)

    def getVertices(self):
        """
        Return the collection of vertex identifiers in the graph.
        :return: A list of vertex identifiers
        """
        return self.vertList.keys()

    def __iter__(self):
        """
        Return an iterator over the vertices in the graph.  This allows the
        user to do:

            for vertex in graph:
                ...

        :return: A list iterator over Vertex objects
        """
        return iter(self.vertList.values())

def getEmployeesAtRisk(graph, edgeOrder):
    # initializing distance and parent arrays
    n = len(graph.vertList.keys())
    d = [float("inf")] * n
    d[0] = 0
    parent = [None] * n

    # iterating n-1 times
    for i in range(n):
        # iterating through the edges in a fixed order everytime
        for edge in edgeOrder:
            src = edge[0]
            dest = edge[1]
            cost = edge[2]
            # updating cost and parent
            if d[dest] > d[src] + cost:
                d[dest] = d[src] + cost
                parent[dest] = src

    # checking for negative cycles
    negativeCycle = False
    visited = set()
    # n'th iteration
    for edge in edgeOrder:
        src = edge[0]
        dest = edge[1]
        cost = edge[2]
        if d[dest] > d[src] + cost:
            # if negative cycle is found, find all reachable vertices, since such vertices
            # can keep using the negative cycle to spiral down endlessly
            visited = reachableWithDFS(dest, visited)
            negativeCycle = True

    # if no negative cycle is found, return 0
    if not negativeCycle:
        return 0
    # if negative cycle is found, return the number of vertices (employees) that can spiral down endlessly
    else:
        return len(visited)

def reachableWithDFS(startKey, visited):
    # find all nodes reachable from a given node
    if startKey in visited:
        return visited
    else:
        visited.add(startKey)
        for neighbour in graph.getVertex(startKey).getConnections():
            visited = reachableWithDFS(neighbour.id, visited)
        return visited

if __name__ == '__main__':
    graph = Graph()

    # vertices represent employee
    n = int(input())
    for i in range(n):
        graph.addVertex(i)

    # edges represent a conversation (initiator, recipient, effect on mood)
    m = int(input())

    # saving the order for looping through the edges later
    edgeOrder = []
    for i in range(m):
        edge = [int(i) for i in input().split()]
        edgeOrder.append(edge)
        src = edge[0]
        dest = edge[1]
        cost = edge[2]
        graph.addEdge(src, dest, cost)

    print(getEmployeesAtRisk(graph, edgeOrder))

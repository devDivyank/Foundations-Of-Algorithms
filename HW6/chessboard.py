"""
file: chessboard.py
description: CSCI-665.04 - HMWK6: Q2 place dominoes on a chessboard perfectly
language: python3
author: Divyank Kulshrestha, dk9924
author: Vineet Singh, vs9779

Implementation for class Graph and class Vertex taken from: 'CSCI-620 - Computational Problem Solving' and modified.
"""

import copy
import math

class Vertex:
    """
    An individual vertex in the graph.

    :slots: id:  The identifier for this vertex (user defined, typically
        a string)
    :slots: connectedTo:  A dictionary of adjacent neighbors, where the key is
        the neighbor (Vertex), and the value is the edge cost (int)
    """

    __slots__ = 'id', 'connectedTo', 'colour', 'occupied'

    def __init__(self, key, colour, occupied):
        """
        Initialize a vertex
        :param key: The identifier for this vertex
        :return: None
        """
        self.id = key
        self.connectedTo = {}
        self.colour = colour
        self.occupied = occupied

    def addNeighbor(self, nbr, weight=0):
        """
        Connect this vertex to a neighbor with a given weight (default is 0).
        :param nbr (Vertex): The neighbor vertex
        :param weight (int): The edge cost
        :return: None
        """
        self.connectedTo[nbr] = weight

    def __repr__(self):
        """
        Return a string representation of the vertex and its direct neighbors:

            vertex-id connectedTo [neighbor-1-id, neighbor-2-id, ...]

        :return: The string
        """
        return f"{str(self.id)}"  # + ' connectedTo: ' + str([str(x.id) for x in self.connectedTo])

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

    def addVertex(self, key, colour, occupied):
        """
        Add a new vertex to the graph.
        :param key: The identifier for the vertex (typically a string)
        :return: Vertex
        """
        # count this vertex if not already present
        if self.getVertex(key) == None:
            self.numVertices += 1
            vertex = Vertex(key, colour, occupied)
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

    def findShortestPath(self, start, end):
        """
        Find the shortest path, if one exists, between a start and end vertex
        :param start (Vertex): the start vertex
        :param end (Vertex): the destination vertex
        :return: A list of Vertex objects from start to end, if a path exists,
            otherwise None
        """
        # Using a queue as the dispenser type will result in a breadth first
        # search
        queue = []
        queue.append(start)         # prime the queue with the start vertex

        # The predecessor dictionary maps the current Vertex object to its
        # immediate predecessor.  This collection serves as both a visited
        # construct, as well as a way to find the path
        predecessors = {}
        predecessors[start] = None  # add the start vertex with no predecessor

        # Loop until either the queue is empty, or the end vertex is encountered
        while len(queue) > 0:
            current = queue.pop(0)
            if current == end:
                break
            for neighbor in current.getConnections():
                if neighbor not in predecessors:        # if neighbor unvisited
                    predecessors[neighbor] = current    # map neighbor to current
                    queue.append(neighbor)              # enqueue the neighbor

        # If the end vertex is in predecessors a path was found
        if end in predecessors:
            path = []
            current = end
            while current != start:              # loop backwards from end to start
                path.insert(0, current)          # prepend current to the path list
                current = predecessors[current]  # move to the predecessor
            path.insert(0, start)
            return path
        else:
            return None

def createGraph(d1, d2):
    # creating the graph
    graph = Graph()
    forwardEdges = set()
    graph.addVertex("Source", None, False)
    graph.addVertex("Sink", None, False)
    blockedCells = set()

    vertexKey = 1
    for i in range(d1):
        for j in range(d2):
            if (i + j) % 2 == 0:
                # white cells - used as the left half of bipartite matching
                if board[i][j] == 1:
                    # if cell is blocked, no edges in or out
                    graph.addVertex(vertexKey, 'White', True)
                    blockedCells.add(vertexKey)
                elif board[i][j] == 0:
                    # edge from 'source' to current cell
                    graph.addVertex(vertexKey, 'White', False)
                    graph.addEdge("Source", vertexKey, 1)
                    forwardEdges.add(("Source", vertexKey))
            elif (i + j) % 2 == 1:
                # black cells - used as the right half of bipartite matching
                if board[i][j] == 1:
                    # if cell is blocked, no edges in or out
                    graph.addVertex(vertexKey, 'Black', True)
                    blockedCells.add(vertexKey)
                elif board[i][j] == 0:
                    # edge from current cell to 'sink'
                    graph.addVertex(vertexKey, 'Black', False)
                    graph.addEdge(vertexKey, "Sink", 1)
                    forwardEdges.add((vertexKey, "Sink"))
            vertexKey += 1

    # adding edges from white cells to black cells - from left to right in bipartite matching
    for i in range(1, (d1 * d2) + 1):
        currentVertex = graph.getVertex(i)
        # if cell is blocked, no edges in or out
        if currentVertex.occupied == True:
            continue
        # if cell is black, no edges in or out
        elif currentVertex.colour == "Black":
            continue
        # if cell is white...
        else:
            # edge to the left cell (if exists and not occupied)
            if 0 < i - 1 and (math.floor((i - 1) / d2) == math.floor(i / d2) or i % d2 == 0):
                if not graph.getVertex(i - 1).occupied:
                    graph.addEdge(i, i - 1, 1)
                    forwardEdges.add((i, i - 1))
            # edge to the right cell (if exists and not occupied)
            if i + 1 <= d1 * d2 and (math.ceil((i + 1) / d2) == math.ceil(i / d2) or i % d2 == 1):
                if not graph.getVertex(i + 1).occupied:
                    graph.addEdge(i, i + 1, 1)
                    forwardEdges.add((i, i + 1))
            # edge to the above cell (if exists and not occupied)
            if 0 < i - d2:
                if not graph.getVertex(i - d2).occupied:
                    graph.addEdge(i, i - d2, 1)
                    forwardEdges.add((i, i - d2))
            # edge to the below cell (if exists and not occupied)
            if i + d2 <= d1 * d2:
                if not graph.getVertex(i + d2).occupied:
                    graph.addEdge(i, i + d2, 1)
                    forwardEdges.add((i, i + d2))

    return graph, forwardEdges, blockedCells


def fordFulkerson(graph, forwardEdges, blockedCells, sourceKey = "Source", sinkKey = "Sink"):
    # creating the residual graph
    residualGraph = copy.deepcopy(graph)
    residualSource = residualGraph.getVertex(sourceKey)
    residualSink = residualGraph.getVertex(sinkKey)
    backwardEdges = set()
    flowingEdges = set()

    # while there is a path from source to sink
    while residualGraph.findShortestPath(residualSource, residualSink):
        path = residualGraph.findShortestPath(residualSource, residualSink)
        i = 0
        j = 1
        # looping through the edges in the path
        while j < len(path):
            edge = (path[i].id, path[j].id)
            backwardEdge = (path[j].id, path[i].id)
            # if a forward edge is found, adding a backward edge
            if edge in forwardEdges:
                flowingEdges.add(edge)
                backwardEdges.add(backwardEdge)
            else:
                # if a backward edge if found, subtracting the flow from forward edge
                if backwardEdge in flowingEdges:
                    flowingEdges.remove(backwardEdge)
            i += 1
            j += 1
        # updating the edges in residualgraph
        for edge in flowingEdges:
            if residualGraph.getVertex(edge[1]) in residualGraph.getVertex(edge[0]).connectedTo:
                residualGraph.getVertex(edge[0]).connectedTo.pop(residualGraph.getVertex(edge[1]))
        for edge in backwardEdges:
            residualGraph.addEdge(edge[0], edge[1], 1)

    # checking if all unoccupied cells have been matched perfectly
    finalMatchings = set()
    for edge in flowingEdges:
        if "Source" in edge or "Sink" in edge:
            continue
        finalMatchings.add(edge)
    for edge in finalMatchings:
        blockedCells.add(edge[0])
        blockedCells.add(edge[1])
    # returning the number of cells that are occupied/covered after placing the dominoes
    return len(blockedCells)


if __name__ == '__main__':
    d1, d2 = tuple([int(i) for i in input().strip().split()])
    # saving the board as a matrix (2D-array)
    board = []
    for i in range(d1):
        row = [int(i) for i in input().strip().split()]
        board.append(row)
    
    graph, forwardEdges, blockedCells = createGraph(d1, d2)
    # if perfect placement is possible, all cells on the board should be either occupied or covered with a domino
    if d1*d2 == fordFulkerson(graph, forwardEdges, blockedCells):
        print("YES")
    else:
        print("NO")


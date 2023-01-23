"""
file: directions.py
description: CSCI-665.04 - HMWK5: Q2 minimum number of instructions to guide the friend to destination
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

    __slots__ = 'id', 'connectedTo', 'incoming', 'outgoing'

    def __init__(self, key):
        """
        Initialize a vertex
        :param key: The identifier for this vertex
        :return: None
        """
        self.id = key
        self.connectedTo = {}
        self.incoming = 0
        self.outgoing = 0

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

def findInstructions(graph: Graph, start: Vertex, end: Vertex):
    """
    Find the shortest path, if one exists, between a start and end vertex

    :param graph: the complete graph
    :param start (Vertex): the start vertex
    :param end (Vertex): the destination vertex
    :return: minimum instructions required to reach the destination
    """

    # Using a queue as the dispenser type will result in a breadth first
    # search
    queue = []
    queue.append(start)
    # keeping track of seen and unseen vertex while traversing
    seen = [False] * len(graph.vertList)
    seen[start.id] = True
    # to keep track of instructions at different steps of BFS
    instructions = [0]

    while queue:
        currentVertex = queue.pop(0)
        # if endpoint is reached
        if currentVertex == end:
            return instructions[0]
        currentInstructions = instructions.pop(0)
        # if multiple paths from vertex
        if len(currentVertex.getConnections()) > 1:
            currentInstructions += 1
        for neighbour in currentVertex.getConnections():
            if seen[neighbour.id] == False:
                # if multiple paths from neighbour
                if len(neighbour.getConnections()) > 2:
                    seen[neighbour.id] = True
                    queue.append(neighbour)
                    instructions.append(currentInstructions)
                # if only one path further from neighbour
                elif len(neighbour.getConnections()) == 2:
                    twoStepNeighbours = []
                    for n in neighbour.getConnections():
                        # if neighbour of neighbour not seen yet
                        if seen[n.id] == False:
                            twoStepNeighbours.append(n)
                    # if atleast one unseen neighbour of neighbour exists
                    if len(twoStepNeighbours) > 0:
                        nextStep = checkNextStep(currentInstructions, seen, queue, instructions, neighbour,
                                                              end, twoStepNeighbours[0])
                        instructions, seen, queue = nextStep
                # if neighbour is destination and also a dead end
                elif len(neighbour.getConnections()) == 1 and neighbour == end:
                    instructions.append(currentInstructions)
                    break
    return instructions[0]

def checkNextStep(currentInstructions, seen, queue, instructions, neighbour, end, twoStepNeighbour):
    """
        checks the numbers of paths two steps from a vertex

        :param currentInstructions: number of intructions till the vertex one step before current neighbour
        :param seen: vertices already seen while traversing
        :param queue: queue for BFS traversal
        :param instructions: instructions required to reach the current point
        :param neighbour: current immediate neighbour of the vertex we are checking
        :param end: destination for the friend
        :param twoStepNeighbour: neighbour of current neighbour (two steps from vertex being checked)
        :return: minimum instructions required to reach the destination
    """
    seen[neighbour.id] = True
    for neighbour in twoStepNeighbour.getConnections():
        # if neighbour of neighbour is destination
        if neighbour == end:
            queue.append(neighbour)
            instructions.append(currentInstructions)
            break
        # if only one path from neighbour of neighbour
        elif len(neighbour.getConnections()) == 2 and seen[neighbour.id] == False:
            # we move further down the path
            return checkNextStep(currentInstructions, seen, queue, instructions, twoStepNeighbour, end, neighbour)
        # if multiple paths from neighbour of neighbour
        elif seen[neighbour.id] == False:
            seen[neighbour.id] = True
            queue.append(neighbour)
            instructions.append(currentInstructions)
            break
    nextStep = (instructions, seen, queue)
    return nextStep

if __name__ == '__main__':
    n = int(input())
    m = int(input())
    graph = Graph()

    # adding vertices to graph
    for i in range(n):
        graph.addVertex(i)
    source = int(input())
    destination = int(input())

    # adding two-way edges to graph
    for i in range(m):
        edge = [int(i) for i in input().split()]
        start = edge[0]
        end = edge[1]
        graph.addEdge(start, end)
        graph.addEdge(end, start)

    # getting start vertex and ending vertex
    startPoint = graph.getVertex(source)
    endPoint = graph.getVertex(destination)

    instructions = findInstructions(graph, startPoint, endPoint)
    print(instructions)

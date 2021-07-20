def readFile():
    f = open("graph2.txt", "r")
    l = []
    line = f.readline()
    while(line):
        lineAux = line.rstrip('\n')
        l.append(lineAux)
        line = f.readline()
    f.close()
    return l
def readAdjacencyMatrix(graphFile):
    adjacencyMatrix = []
    i = 2
    while (i < len(graphFile)):
        adjacency = graphFile[i].split(",")
        j = 0
        #Parse all elements Strings to Int
        while(j < len(adjacency)):
            adjacency[j] = int(adjacency[j])
            j+=1
        adjacencyMatrix.append(adjacency)
        i+=1
    return adjacencyMatrix
def buildGraph():
    graph = []
    adjacencyMatrix = []
    graphFile = readFile()
    #Save number of vertices
    vertices = int(graphFile[0])
    #Save number of edges
    edges = int(graphFile[1])
    #Save adjacency matrix
    adjacencyMatrix = readAdjacencyMatrix(graphFile)
    #Build the Graph
    graph.append(vertices)
    graph.append(edges)
    graph.append(adjacencyMatrix)
    return graph
if __name__ == '__main__':
    graph = buildGraph()
    print("Graph")
    print(graph)

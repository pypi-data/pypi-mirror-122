

def Bellmanford(graph,source,numvertex):
    distance = []
    for i in range(numvertex):
        distance.append(float('inf'))
    distance[source] = 0

    for i in range(numvertex - 1):
        for u in range(numvertex):
            for k in range(len(graph[u])):
                v,cost = graph[u][k]
                if distance[u] + cost < distance[v]:
                    distance[v] = distance[u] + cost

    return distance

def how_to():
    print("the function expects a graph represented as a adjacency list, import howToGraph and use the function\nhow_to() to see how the implement the graph as a dictionary of lists")
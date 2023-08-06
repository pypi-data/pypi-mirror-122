#Representating a graph as a adjacency list and as a adjancecy matrix using a dictionary


def how_to():
    print("let n be the number of vertices of a graph:\n")
    print("The graph can be implemented as a adjancency list as follows:\n graph = {} \n for i in range(n): \n     graph[i] = []\n Now in order to add a pair u,v with a weight between u and v do:\n graph[u].append((v,weight))")
    print("the graph can be implemented as a adjacency matrix as follows:\n graph = {} \n for i in range(n): \n     graph[i] = []\n for i in range(n):\n     for j in range(n):\n           graph[i].append(float('inf'))\n Now if vertices u and v are connected, do \n graph[u][v] = weight ")


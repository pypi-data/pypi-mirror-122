

def Floydwarshall(graph,numvertex):
    
    dist = graph 
    for k in range(numvertex):
        for i in range(numvertex):
            for j in range(numvertex):
                if dist[i][j] > (dist[i][k] + dist[k][j]) and (dist[k][j] != float('inf') and dist[i][k] != float('inf')):
                    dist[i][j] = dist[i][k] + dist[k][j]
    

    return dist

def how_to():
    print("Use a adjacency matrix to use the algorithm, if vertices u and v are not connected,\n the graph[u][v] = float('inf')")


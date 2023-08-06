import heapq

def Dijkstra(graph,source,target,numvertex):
    print("")
    distance = []
    for i in range(numvertex):
        distance.append(float('inf'))
    distance[source] = 0

    q = []
    heapq.heapify(q)
    heapq.heappush(q,(0,source))

    while len(q) != 0:
        c,u = heapq.heappop(q)
        for i in range(len(graph[u])):
            v,cost = graph[u][i]
            if distance[v] > distance[u] + cost:
                distance[v] = distance[u] + cost
                heapq.heappush(q,(distance[v],v))
    return distance

def how_to():
    print("the function expects a graph represented as a adjacency list, import Graph and use the function\nhow_to() to see how the implement the graph as a dictionary of lists")


import sys
from collections import deque
def ball(node,r):
    q = deque()
    k = []
    visited = [False for k in g.keys()]
    inqueue = [False for k in g.keys()]
    weight = [0 for k in g.keys()]
    for i in range(int(sys.argv[3])+1):
        visited.append(False)
        inqueue.append(False)
        weight.append(0)
    q.appendleft(node)
    inqueue[node]=True
    while not (len(q) == 0):
        c = q.pop()
        inqueue[c] = False
        visited[c] = True
        for v in g[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
                weight[v] = weight[c]+1
                if weight[v] <= r:
                    k.append(v)
    return k
def tball(node,r):
    q = deque()
    k=[]
    visited = [False for k in g.keys()]
    inqueue = [False for k in g.keys()]
    weight = [0 for k in g.keys()]
    for i in range(int(sys.argv[3]) + 1):
        visited.append(False)
        inqueue.append(False)
        weight.append(0)
    q.appendleft(node)
    inqueue[node]=True
    while not (len(q) == 0):
        c = q.pop()
        inqueue[c] = False
        visited[c] = True
        for v in g[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
                weight[v]= weight[c]+1
                if weight[v]==r:
                    k.append(v)
    return k
if sys.argv[1]=='-c':
    input_filename = sys.argv[3]
    g = {}
    with open(input_filename) as graph_input:
        for line in graph_input:
            # Split line and convert line parts to integers.
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            # If a node is not already in the graph
            # we must create a new empty list.
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            # We need to append the "to" node
            # to the existing list for the "from" node.
            g[nodes[0]].append(nodes[1])
            # And also the other way round.
            g[nodes[1]].append(nodes[0])
    reverse = {}
    for x in range(int(sys.argv[2])):
        degree = dict([(z, 0) for z in g])
        for i in g.values():
             for y in i:
                 degree[y] +=1
        reverse = {k: v for k, v in sorted(degree.items(), key=lambda item: item[1], reverse=True)}
        a = list(reverse.keys())[0]
        b= degree[a]
        for i in reverse.keys():
            if degree[a] == degree[i] and a>i:
                a=i
        g.pop(a)
        for i in g.values():
            if (a) in i:
                i.remove(a)
        print(a, b, sep=" ")
if sys.argv[1]=="-r":
    input_filename = sys.argv[4]
    g = {}
    with open(input_filename) as graph_input:
        for line in graph_input:
            # Split line and convert line parts to integers.
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            # If a node is not already in the graph
            # we must create a new empty list.
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            # We need to append the "to" node
            # to the existing list for the "from" node.
            g[nodes[0]].append(nodes[1])
            # And also the other way round.
            g[nodes[1]].append(nodes[0])
    r = int(sys.argv[2])
    degree = dict([(z, 0) for z in g])
    for i in g.values():
         for y in i:
            degree[y] += 1
    ci = dict([(z, 0) for z in g])
    for i in g:
        sum = 0
        for y in tball(i , r):
            sum += (degree[y]-1)
            ci[i] =sum * (degree[i]-1)
    for x in range(int(sys.argv[3])):
        reverse = {k: v for k, v in sorted(ci.items(), key=lambda item: item[1], reverse=True)}
        a= next(iter(reverse))
        b = reverse[a]
        for i in reverse.keys():
            if ci[a] == ci[i] and a>i:
                a=i
        print(a, b, sep=" ")
        affected=ball(a,r+1)
        g.pop(a)
        ci.pop(a)
        for i in g.values():
            if (a) in i:
                i.remove(a)
        for k in g.keys():
            if k in affected:
                degree[k] = (len(g[k]))
        for i in g:
            if i in affected:
                sum = 0
                for k in tball(i, r):
                    sum += (degree[k] - 1)
                ci[i] = sum * (degree[i] - 1)

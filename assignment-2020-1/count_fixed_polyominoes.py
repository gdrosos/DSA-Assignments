import pprint
import sys
g = {}
check = False
if sys.argv[1] == "-p":
    sys.argv[1], sys.argv[2] = sys.argv[2], sys.argv[1]
    check = True
for i in range(2 - int(sys.argv[1]), int(sys.argv[1])):
    for j in range(int(sys.argv[1])):
        if i == 0 and j == 0:
            g[(i, j)] = [(i + 1, j), (i, j + 1)]
        elif (i < 0 and j == 1 and j - i == int(sys.argv[1]) - 1):
            g[(i, j)] = [(i + 1, j)]
        elif (i < 0 and j == 0):
            continue
        elif (abs(i) + abs(j) > int(sys.argv[1]) - 1):
            continue;
        elif (i < 0 and j == 1):
            g[(i, j)] = [(i + 1, j), (i, j + 1), (i - 1, j)]
        elif (i < 0 and j - i == int(sys.argv[1]) - 1):
            g[(i, j)] = [(i + 1, j), (i, j - 1)]
        elif (j == 0 and i + j == int(sys.argv[1]) - 1):
            g[(i, j)] = [(i - 1, j)]
        elif (j == 0):
            g[(i, j)] = [(i + 1, j), (i, j + 1), (i - 1, j)]
        elif (i + j == int(sys.argv[1]) - 1 and i == 0):
            g[(i, j)] = [(i, j - 1)]
        elif (i + j == int(sys.argv[1]) - 1):
            g[(i, j)] = [(i - 1, j), (i, j - 1)]
        else:
            g[(i, j)] = [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]
if check:
    pprint.pprint(g)
n = int(sys.argv[1])
untried = {(0, 0)}
p = []
c = 0
temp = 0
def neighbours(i, p, u, k):
    p_not_u = set(p) - set([u])
    for l in p_not_u:
        k.update(g[l])
    if i not in k:
        return True
    else:
        return False
def cfp(g, untried, n, p, c):
    global temp
    while len(untried) != 0:
        u = untried.pop()
        p.append(u)
        if len(p) == n:
            c += 1
        else:
            k = set()
            new_neighbours = set()
            for i in g[u]:
                if i not in untried and i not in p and neighbours(i, p, u, k):
                    new_neighbours.add(i)
            new_untried = untried | new_neighbours
            cfp(g, new_untried, n, p, c)
        p.remove(u)
    temp += c
    return c
cfp(g, untried, n, p, c)
print(temp)

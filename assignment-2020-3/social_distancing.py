import argparse
import math
import random

def efaptomenos(cm, cn,r):
    dx = cn[0] - cm[0]
    dy = cn[1] - cm[1]
    d = math.sqrt(dx * dx + dy * dy)
    r1 = cm[2] + r
    r2 = cn[2] + r
    l = (r1 * r1 - r2 * r2 + d * d) / (2 * d * d)
    e = math.sqrt(((r1 * r1) / (d * d)) - (l * l))
    a = round(cm[0] + l * dx - e * dy, 2)
    b = round(cm[1] + l * dy + e * dx, 2)
    return a, b, r


def distance(c1, c2):
    d = math.sqrt((c1[0] - c2[0]) * (c1[0] - c2[0]) + (c1[1] - c2[1]) * (c1[1] - c2[1]))
    return round(d, 2)


def print_circles(c):
    f = open(file, "w")
    for i in c:
        f.write(str(i[0]))
        f.write(' ')
        f.write(str(i[1]))
        f.write(' ')
        f.write(str(i[2]))
        f.write('\n')
    return f


# check if c1 is before c2 in the front
def check_direction(c1, c2, g):
    count = 0
    while True:
        count = count + 1
        temp = g[c1]
        c1 = temp
        if c1 == c2:
            break
    if len(g) - count > count:
        return True
    return False


# removes circles from the circle next to c1 to the one before c2 from the front
def remove_circles(c1, c2, g):
    first = g[c1]
    while True:
        temp = g[first]
        g.pop(first)
        first = temp
        if first == c2:
            break
    g[c1] = c2
    return g


def find_cj(cn, cm, ci, g):
    count = 0
    list1 = []
    list2 = []
    cn1 = cn
    while True:
        a = g[cn1]
        if a == cm:
            break
        if distance(a, ci) < a[2] + ci[2]:
            list1.append(a)
            list2.append(count)
        count = count + 1
        cn1 = a
    if len(list1) == 0:
        return None
    if len(list1) == 1:
        return list1[0]
    count = 0
    k = list1.pop()
    while True:
        a = g[k]
        if a == cm:
            break
        count = count + 1
        k = a
    bnj = list2[0]
    bmj1 = count
    if bmj1 < bnj:
        return k
    else:
        return list1[0]


def distance_from_boundary(c, u, v):
    l2 = (u[0]-v[0]) * (u[0]-v[0]) + (u[1]-v[1]) * (u[1]-v[1])
    if l2 == 0:
        d = math.sqrt((u[0]-c[0]) * (u[0]-c[0]) + (u[1]-c[1]) * (u[1]-c[1]))
    else:
        t = ((c[0]-u[0]) * (v[0] - u[0]) + (c[1]-u[1]) * (v[1] - u[1]))/l2
        if t > 1:
            t = 1
        elif t < 0:
            t = 0
    px = u[0] + t * (v[0] - u[0])
    py = u[1] + t * (v[1] - u[1])
    d = math.sqrt((px-c[0]) * (px-c[0]) + (py-c[1]) * (py-c[1]))
    d = round(d, 2)
    if c[2] <= d:
        return False
    else:
        return True


def read_boundary(x):
    l = []
    with open(x) as list_input:
        for line in list_input:
            nodes = [float(x) for x in line.split()]
            if len(nodes) != 4:
                continue
            b1 = [nodes[0], nodes[1]]
            b2 = [nodes[2], nodes[3]]
            c = [b1, b2]
            l.append(c)
    return l


def check_collision(c, l):
    for i in l:
        if distance_from_boundary(c, i[0], i[1]):
            return True
    return False


def print_boundary(f):
    with open(args.boundary_file) as i:
        f.write(i.read())

# variable check1 is True when there is a specific r (-r) given, same for all circles
# variable check2 is True when there is a boundary file
# variable check3 is True when there is a specific circle number (-i) given

check2 = False
check3 = False
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--items", type=int)
parser.add_argument("-r", "--radius", type=int)
parser.add_argument("--seed", "--seed", type=int)
parser.add_argument("--min_radius", type=int)
parser.add_argument("--max_radius", type=int)
parser.add_argument("-b", "--boundary_file")
parser.add_argument("filename", help="name of output file")
args = parser.parse_args()
if args.items:
    items = args.items
    check3 = True
if args.radius:
    r = args.radius
    check1 = True
if args.seed:
    random.seed(args.seed)
    check1 = False
if args.min_radius:
    min1 = args.min_radius
if args.max_radius:
    max1 = args.max_radius
if args.boundary_file:
    boundary_list = read_boundary(args.boundary_file)
    check2 = True
file = args.filename
circles = []
if check1:
    first = (0.00, 0.00, r)
    second = (2 * r, 0.00, r)
else:
    first = (0.00, 0.00, random.randint(min1, max1))
    r = random.randint(min1, max1)
    second = (first[2] + r, 0.00, r)
circles.append(first)
circles.append(second)
if check2:
    living = []
    living1 = []
    front1 = {}
    total_cms = []
    living.append(first)
    living.append(second)
front = {
    first: second,
    second: first
}
reverse = {}
# variable check is true when we need to find the closest circle to the begin
# variable check4 is used when we have a boundary file and random radius, and checks if we need to find a new radius
check = True
check4 = True
if check3:
    loop_check = len(circles) < items
else:
    loop_check = True
while loop_check:
    if check2:
        if len(living) == 0:
            break
    if check:
        distances = {}
        for j in front:
            if check2:
                if j in living:
                    distances[j] = distance(j, (0.00, 0.00, r))
            else:
                distances[j] = distance(j, (0.00, 0.00, r))
        reverse = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1], reverse=False)}
        a = list(reverse.items())[0][1]
        for k in circles:
            if k in front:
                if check2:
                    if k in living:
                        if distances[k] == a:
                            cm = k
                            total_cms.append(cm)
                            break
                else:
                    if distances[k] == a:
                        cm = k
                        break
        value = cm
        cn = front[cm]
        if not check1:
            if check2:
                if check4:
                    r = random.randint(min1, max1)
            else:
                r = random.randint(min1, max1)
    ci = efaptomenos(cm, cn, r)
    cj = find_cj(cn, cm, ci, front)
    if cj == None:
        if check2:
            if check_collision(ci, boundary_list):
                living = living1[:]
                front = dict(front1)
                for i in total_cms:
                    if i in living:
                        living.remove(i)
                if value in living:
                    living.remove(value)
                check = True
                check4 = False
            else:
                circles.append(ci)
                front[cm] = ci
                front[ci] = cn
                total_cms = []
                for i in front:
                    if i not in living:
                        living.append(i)
                check = True
                check4 = True
                front1 = dict(front)
                living1 = living[:]
        else:
            circles.append(ci)
            front[cm] = ci
            front[ci] = cn
            check = True
    else:
        if check_direction(cj, cm, front):
            front = remove_circles(cj, cn, front)
            if check2:
                for i in living:
                    if i not in front:
                        living.remove(i)
            cm = cj
            check = False
        elif check_direction(cn, cj, front):
            front = remove_circles(cm, cj, front)
            if check2:
                for i in living:
                    if i not in front:
                        living.remove(i)
            cn = cj
            check = False
    if check3:
        loop_check = len(circles) < items
print_circles(circles)
print(len(circles))
if check2:
    print_boundary(print_circles(circles))

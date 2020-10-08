import numpy as np
from skimage.draw import line
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from itertools import product

def dist(x1,x2):
    return np.sqrt(np.sum(np.square(np.array(x1)-np.array(x2)), axis=0))

def angle(x1,x2):
    return np.arctan2(x2[1]-x1[1],x2[0]-x1[0])

def get_eq(x, axis,verbose=False):
    if axis == 0:
        (x1,y1),(x2,y2) = x
    else:
        (y1,x1),(y2,x2) = x
    dy = y2-y1
    dx = x2-x1
    if dx == 0: 
        return lambda x: np.inf # not rigorous; see how constraint() handles this case
    slope = dy/dx
    shift = (y1+y2)/2 - slope * (x1+x2)/2
    if verbose:
        if axis == 0:
            y = 'y'
            x = 'x'
        else:
            y = 'x'
            x = 'y'
        print('{} = {}{} + {}'.format(y,slope,x,shift))
    return lambda x: slope*x + shift

def constraint(f, parity, orientation):
    if f(0) == np.inf:   
    # orthogonal to the oriented axis, so "discard" this constraint in final and'd fn
        return lambda x: True
    else:
        if parity == 1:
            return lambda x: x[orientation-1] <= f(x[orientation])
        elif parity == -1:
            return lambda x: x[orientation-1] > f(x[orientation])

# a,b : give the line over which the algorithm iterates
# axis and parity : specify the direction in which strips are generated, 
#       e.g., axis=0 parity=1 will increment the x-value of a point in ab until the constraint is no longer satisfied
# constraint : returns true if x is within the triangle and false otherwise
def tri_bresenham(a, b, axis, parity, constraint, verbose=False):
    ab = X,Y = line(a[0],a[1],b[0],b[1])
    n = len(X)
    points = []
    prev_row = -1
    for i in range(n):
        # iterate over each unique column index
        curr_row = ab[axis][i]
        if curr_row == prev_row:    continue
        # mutable position vector
        x = [X[i],Y[i]]
        # temp container for traversed points
        col = []
        # while within the constraints of the triangle,
        while constraint(x):
            # collect points
            col.append((x[0],x[1]))
            if verbose:
                print(x)
            # and march forward as per axis & parity (dimension and direction)
            x[axis-1] += parity
        points.extend(col)
        if verbose: print(col)
        prev_row = curr_row
    if verbose: print(points)
    return points

# a,b,c : vertices of the triangle in (x,y) form
def fill_tri(a,b,c,verbose=False):
    # organize the triangle by longest side and not-longest sides
    sides = [(a,b),(b,c),(c,a)]
    ax_idx = np.argmax([dist(x[0],x[1]) for x in sides])
    ax = sides[ax_idx]
    ax_ang = angle(ax[0],ax[1])
    c1,c2 = sides[ax_idx-1],sides[ax_idx-2]
    assert c1[0] == c2[1]
    # find the vertex, t, not on the longest side
    t = c1[0] 
    # determine the orientation of the triangle
    if np.pi/4 <= ax_ang < 3*np.pi/4 or -3*np.pi/4 <= ax_ang < -np.pi/4:
        orientation = 1
    else:
        orientation = 0
    # find line f describing AB
    f = get_eq(ax,orientation,verbose=verbose)
    # determine the parity of the triangle
    if f(t[orientation]) < t[orientation-1]:
        parity = 1
    else:
        parity = -1
    if verbose:
        print('axial:\t\t',ax)
        print('angle:\t\t',ax_ang)
        print('third:\t\t',t)
        print('orientation:\t',orientation)
        print('parity:\t\t',parity)
    #   find lines g(y),h(y) describing BC,AC
    g = get_eq(c1,orientation,verbose=verbose)
    h = get_eq(c2,orientation,verbose=verbose)
    #   construct constraints per parity
    under_g = constraint(g, parity, orientation)
    under_h = constraint(h, parity, orientation)
    # get points as constrained by ax and g,h
    points = tri_bresenham(ax[0],ax[1],orientation,parity,
            constraint=lambda x: under_g(x) and under_h(x), verbose=verbose)
    return points

import sys
if len(sys.argv) > 4:   raise ValueError('too many arguments')
Vstr = sys.argv[1:]
V = [(int(vs.split(',')[0]), int(vs.split(',')[1])) for vs in Vstr]
a,b,c = V
X = [v[0] for v in V]
Y = [v[1] for v in V]
width = max(X) - min(X) + 2
height = max(Y) - min(Y) + 2
points = fill_tri(a,b,c, verbose=True)
print(len(points))
im = np.zeros((width,height))
offx = min(X)
offy = min(Y)
points = [(p[0]-offx,p[1]-offy) for p in points]
print(points)
for x,y in points:
    im[x,y] = 1
from matplotlib import pyplot as plt
plt.imshow(im)
plt.show()

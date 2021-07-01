import numpy as np
from skimage.draw import line

def dist(x1,x2):
    """
    euclidian distance / norm
    :param x1: a numeric 2-tuple
    :param x2: another numeric 2-tuple
    :return: magnitude of the vector between `x1` and `x2`
    """
    # ((x_f - x_i)^2 + (y_f - y_i)^2)^{1/2}
    return np.sqrt(np.sum(np.square(np.array(x1)-np.array(x2)), axis=0))

def angle(x1,x2):
    """
    angle (in radians!) between two vectors.
    :param x1: the destination of a vector rooted at (0,0)
    :param x2: the destination of another vector rooted at (0,0)
    :return: an angle in [-pi and pi] between two vectors
    """
    # \tan^{-1}((y_f - y_i) / (x_f - x_i))
    return np.arctan2(x2[1]-x1[1],x2[0]-x1[0])

def get_eq(segment, axis, verbose=False):
    """
    given a segment and an oriented axis, find the line containing that segment.
    :param segment: two points defining a line segment
    :param axis: determines the orientation of the plane,
                 i.e., which axis is x and which axis is y.
    :return: a function f(x) = a*y + b, defining the line containing `segment`
    """
    # parse `segment` according to the oriented axis
    if axis == 0:
        (x1,y1),(x2,y2) = segment
    elif axis == 1:
        (y1,x1),(y2,x2) = segment
    else:
        raise NotImplementedError("only the two-dimensional case is supported.")
    # differences along each axis
    dy = y2-y1
    dx = x2-x1
    if dx == 0:
        # see `constraint()` for an explanation of this ugliness
        return lambda w: np.inf
    # calculate the ascent and origin of the line
    slope = dy/dx
    shift = (y1+y2)/2 - slope * (x1+x2)/2
    if verbose:
        # give the equation
        if axis == 0:
            y = 'y'
            x = 'x'
        else:
            y = 'x'
            x = 'y'
        print('{} = {}{} + {}'.format(y,slope,x,shift))
    return lambda w: slope*w + shift

def constraint(f, orientation, parity):
    """
    uses a line `f` to construct a partition of the euclidian plane
    :param f: a linear equation |R -> |R, f(x) = y
    :param orientation: determines the orientation of the plane,
                        i.e., which axis is x and which axis is y.
    :param parity: determines the direction traversed along the oriented axis
    :return: a function that labels points in the plane, per the partition.
    """
    if f(0) == np.inf:
        # orthogonal to oriented axis: this constraint can safely be ignored
        return lambda x: True
    else:
        # not orthogonal
        if parity == 1:
            # assigns label "True" to the half-plane /below/ f
            return lambda x: x[orientation-1] <= f(x[orientation])
        elif parity == -1:
            # assigns label "True" to the half-plane /above/ f
            return lambda x: x[orientation-1] > f(x[orientation])
        else:
            raise ValueError("parity must be +- 1")

def tri_bresenham(segment, axis, parity, constraint, verbose=False):
    """
    modifies bresenham's line algorithm to find the points within a triangle.
    todo - accept arbitrarily many columns ~ dimensions
    :param segment: points describing the oriented side of the triangle
    :param axis: the axis along which bresenham's algorithm traverses
    :param parity: the direction in which bresenham's algorithm traverses
    :param constraint: heuristic for point-triangle intersection
    :param verbose: print debugging info
    :return: a list of all pixels for which `constraint` evaluates to True
    """
    a,b = segment
    ab = X,Y = line(a[0],a[1],b[0],b[1])
    assert len(X) == len(Y)
    n = len(X)
    points = []
    prev_row = -1
    for i in range(n):
        # iterate over each unique column index
        curr_row = ab[axis][i]
        if curr_row == prev_row:
            continue
        # mutable position vector
        x = [X[i],Y[i]]
        # temp container for traversed points
        col = []
        # within the triangle
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

def fill_tri(tri,verbose=False):
    """
    wrapper for the tri_bresenham routine; generates all points within a
    triangle. requires time and space linear to the area of the triangle.
    :param tri: a triangle, described by its three vertices points.
    :param verbose: print debugging info
    :return: a list containing all points that fall within the triangle
    """
    a,b,c = tri
    # locate the longest side `ax` of the triangle
    sides = [(a,b),(b,c),(c,a)]
    ax_idx = np.argmax([dist(x[0],x[1]) for x in sides])
    ax = sides[ax_idx]
    ax_ang = angle(ax[0],ax[1])
    # find the vertex opposing `ax`
    c1,c2 = sides[ax_idx-1],sides[ax_idx-2]
    assert c1[0] == c2[1]
    t = c1[0]
    # orient the triangle to an axis (per the closest to `ax`)
    if np.pi/4 <= ax_ang < 3*np.pi/4 or -3*np.pi/4 <= ax_ang < -np.pi/4:
        orientation = 1
    else:
        orientation = 0
    # find the line containing `ax`
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
    # lines containing the other two sides of the triangle
    g = get_eq(c1,orientation,verbose=verbose)
    h = get_eq(c2,orientation,verbose=verbose)
    # build constraints with regard to the oriented side
    under_g = constraint(g, orientation, parity)
    under_h = constraint(h, orientation, parity)
    print(under_g,under_h)
    # the points above f and below g,h - which makes up the whole triangle!
    points = tri_bresenham(ax, orientation, parity,
                           constraint=lambda x: under_g(x) and under_h(x),
                           verbose=verbose)
    return points

def main():
    import sys
    errstr = "your input didn't make sense!\n"
    errstr += "\ntry something like this:\n"
    errstr += "\tpython try_raster.py u,v w,x y,z\n"
    errstr += "where u,...,z are whole numbers."
    if len(sys.argv) != 4:
        raise ValueError(errstr)
    Vstr = sys.argv[1:]
    V = [(int(vs.split(',')[0]), int(vs.split(',')[1])) for vs in Vstr]
    a,b,c = V
    if not all([len(x) == 2 for x in V]):
        raise ValueError(errstr)
    X = [v[0] for v in V]
    Y = [v[1] for v in V]
    width = max(X) - min(X) + 2
    height = max(Y) - min(Y) + 2
    points = fill_tri([a,b,c], verbose=True)
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

if __name__ == '__main__':
    main()

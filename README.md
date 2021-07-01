# tri_raster
a routine that generates all points in a triangle, requiring time and space linear to its area.

### why do
when i wrote this (oct 2020), the shapely / scikit-image functions for finding points w/in a triangle 
(or any convex polygon, by extension) checked every point in the shape's bounding rectangle.
that seemed kind of silly to me, so i made this. 
i don't know if any of the aforementioned packages have changed their implementations of that function, 
but if they haven't, this routine is ~~better~~* faster.

*beware, here be bugs. albeit, they are trivial bugs, but i'm not fixing them until tomorrow.

### how do
the script requires numpy and scikit-image. 
most recently tested on
```
python=3.9.5
numpy=1.20.2
scikit-image=0.18.1
```

examples:
```
from tri_raster import fill_tri
triangle_vertices = [(0,0),(10,1),(3,21)]

# note: regardless of the vertex values, these points will be relative to the upper leftmost point.
points_in_tri = fill_tri(triangle_vertices) 
```
alternately,
`python tri_raster.py 0,0 10,1 3,21`
will render the triangle inside its bounding rectangle.

### to do
stop orienting the longest axis b/c sometimes it breaks the parity logic (e.g. 0,0 10,1 3,20) -> soln: optimize for axial alignment first, length second; this also picks the most efficient alignment for right triangles, which is cool. 

refactor `tri_bresenham` so as to not require `skimage.draw.line`

implement in c++

notebook to demonstrate performance boost

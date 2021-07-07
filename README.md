# tri_raster
a routine that generates all points in a triangle, requiring time and space linear to its area.

### why do
when i wrote this (oct 2020), the shapely / scikit-image functions for finding points w/in a triangle (or any convex polygon, by extension) checked every point in the shape's bounding rectangle.
that seemed kind of silly to me, so i made this. bresenham's line algorithm is used first to generate points along one side of the triangle, and second to march outwards from each of those points to fill in the shape.
i don't know if any of the aforementioned packages have changed their implementations of that function, but if they haven't, this routine is better*.

*at least, it's linear and it's reliable.

### how do
the script requires numpy and scikit-image (and jupyter, if you want to interact with the test notebook.)
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
points_in_tri = fill_tri(triangle_vertices)
```
alternatively, `python tri_raster.py 0,0 10,1 3,21` will render the triangle inside its bounding rectangle.

### to do
debug fill_tri

refactor `tri_bresenham` so as to not require `skimage.draw.line`

implement in c++

# tri_raster
A routine that generates all points in a triangle, requiring time and space linear to its area.

### why do
When I wrote this in October 2020, the `shapely` and `scikit-image` functions for triangle rasterization checked _every point_ in the shape's bounding rectangle. In the worst case, this method has polynomial time complexity. I needed a worst-case linear algorithm for an image processing project, so I made this. Bresenham's line algorithm is used, first to generate points along one side of the triangle, and second to march outwards from each of those points to fill in the shape.

The new Julia script implements another algorithm as described in <a href="http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html"> Software Rasterization Algorithms for Filling Tirangles </a>. This algorithm is a little faster than the Python version.

### how do
The Python script requires numpy and scikit-image (and jupyter, if you want to interact with the test notebook.)
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

The Julia script has no dependencies!
most recently tested on Julia 1.7.0.

### to do
- refactor `tri_raster.py` to implement the algorithm in `tri_raster.jl`
- implement in c++


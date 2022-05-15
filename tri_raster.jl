module TriRaster

export Triangle, rasterize, geometric_area, d, flatten, variance, average

using Random

"""
A wrapper for the 3-tuple of 2-tuples of integers.
This is probably unnecessary, but OOP habits die hard."""
struct Triangle
    simplex::Tuple{Tuple{Int, Int}, Tuple{Int, Int}, Tuple{Int, Int}}
    Triangle(simplex::Tuple{Tuple{Int, Int}, Tuple{Int, Int}, Tuple{Int, Int}}) = new(simplex)
    Triangle((ax, ay), (bx, by), (cx, cy)) = new(((ax,ay),(bx,by),(cx,cy)))
    Triangle(ax, ay, bx, by, cx, cy) = new(((ax,ay),(bx,by),(cx,cy)))
end

function Base.getindex(TRI::Triangle, i::Int64)
    return TRI.simplex[i]
end

function Base.getindex(TRI::Triangle, i::Int, j::Int)
    return TRI.simplex[i][j]
end

"Evaluate the trigonometric formula for the area of a triangle."
function geometric_area(TRI::Triangle)
    a = d(TRI[1], TRI[2])
    b = d(TRI[1], TRI[3])
    γ = atan((TRI[2] .- TRI[1])...) - atan((TRI[3] .- TRI[1])...)
    return 0.5 * abs(a*b*sin(γ))
end

# Utility functions

d(x1, x2) = sqrt(sum((x1 .- x2).^2))

flatten(P) = [(P...)...] # equivalently, `collect(Iterators.flatten(P))`

"Variance of `IMG` restricted to the sublattice spanned by `TRI`."
variance(IMG, TRI::Triangle) = var([IMG[i, j] for (i,j) in rasterize(TRI)])

"Average of `IMG` restricted to the sublattice spanned by `TRI`."
average(IMG, TRI::Triangle) = mean([IMG[i, j] for (i,j) in rasterize(TRI)])

"Iterate the sublattice of ℤ² intersected by `TRI`."
function rasterize(TRI)
    # sort in vertically-ascending order
    lo, md, hi = vertices = sort([v for v in TRI.simplex], by = v -> v[2])
    x1, y1 = lo
    x2, y2 = md
    x3, y3 = hi
    @assert y1 ≤ y2 ≤ y3
    if y2 == y3
        # bottom-flat triangle
        return _rasterize_bf(TRI)
    elseif y1 == y2
        # top-flat triangle
        return _rasterize_tf(TRI)
    else
        # decompose the triangle into top-flat and bottom-flat regions
        y4 = y2
        x4 = round(Int, x1 + ((y2 - y1) / (y3 - y1)) * (x3 - x1))
        md2 = (x4, y4)
        BTM = Triangle(lo, md, md2)
        TOP = Triangle(md, md2, hi)
        return union(_rasterize_bf(BTM), _rasterize_tf(TOP))
    end
end

"Iterate the sublattice of ℤ² intersected by `TRI`. Case 1: `TRI` is bottom-flat."
function _rasterize_bf(TRI)
    # sort in vertically-ascending order
    lo, md, hi = vertices = sort([v for v in TRI.simplex], by = v -> v[2])
    x1, y1 = lo
    x2, y2 = md
    x3, y3 = hi
    @assert y1 < y2 == y3
    # inverse slopes
    invslope1 = (x2 - x1) / (y2 - y1)
    invslope2 = (x3 - x1) / (y3 - y1)
    # left, right bounds
    lx = x1
    rx = x1
    # iterate lattice points
    lines = Vector{Vector{Tuple{Int, Int}}}()
    for y in y1:y2
        minx = round(Int, min(lx, rx))
        maxx = round(Int, max(lx, rx))
        push!(lines, [(x, y) for x in minx:maxx])
        lx += invslope1
        rx += invslope2
    end
    return flatten(lines)
end

"Iterate the sublattice of ℤ² intersected by `TRI`. Case 2: `TRI` is top-flat."
function _rasterize_tf(TRI)
    # sort in vertically-ascending order
    lo, md, hi = vertices = sort([v for v in TRI.simplex], by = v -> v[2])
    x1, y1 = lo
    x2, y2 = md
    x3, y3 = hi
    @assert y1 == y2 < y3
    # inverse slopes
    invslope1 = (x3 - x1) / (y3 - y1)
    invslope2 = (x3 - x2) / (y3 - y2)
    # left, right bounds
    lx = x3
    rx = x3
    # iterate lattice points
    lines = Vector{Vector{Tuple{Int, Int}}}()
    for y in Iterators.reverse(y1:y3)
        minx = round(Int, min(lx, rx))
        maxx = round(Int, max(lx, rx))
        push!(lines, [(x, y) for x in minx:maxx])
        lx -= invslope1
        rx -= invslope2
    end
    return flatten(lines)
end

end

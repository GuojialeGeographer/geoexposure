# -*- coding: utf-8 -*-
"""Regular grid generation (square fishnet and hexagonal) with CRS validation."""
import math

import geopandas as gpd
from shapely.geometry import box, Polygon


def _validate_projected_boundary(boundary_gdf, cell_size):
    """Shared input guard: require a projected CRS and a positive cell size."""
    if boundary_gdf.crs is None:
        raise ValueError("Boundary has no CRS defined.")
    if boundary_gdf.crs.is_geographic:
        raise ValueError("Use a projected CRS (e.g. EPSG:32632); degrees distort distance/area.")
    if cell_size <= 0:
        raise ValueError("cell_size must be positive.")


def _clip_and_index(cells, crs, boundary_gdf, clip):
    """Build the GeoDataFrame, optionally keep whole cells intersecting the
    boundary, and assign a clean integer ``grid_id``."""
    grid = gpd.GeoDataFrame(geometry=cells, crs=crs)
    if clip:
        poly = boundary_gdf.union_all() if hasattr(boundary_gdf, "union_all") else boundary_gdf.unary_union
        grid = grid[grid.intersects(poly)].copy()
    grid["grid_id"] = range(len(grid))
    return grid.reset_index(drop=True)


def create_regular_grid(boundary_gdf, cell_size, clip=True):
    """Build a regular square grid (fishnet) covering a boundary polygon.

    Square cells align cleanly with a square census grid (1:1), which makes
    them the natural choice for the population-weighted exposure step.

    Parameters
    ----------
    boundary_gdf : GeoDataFrame  研究区边界，必须是投影坐标系
    cell_size : float            网格边长（CRS 单位，UTM 下即米）
    clip : bool                  True 时只保留与边界相交的网格（整格保留，不切割）

    Returns
    -------
    GeoDataFrame  含 'grid_id' 列，CRS 与输入一致
    """
    _validate_projected_boundary(boundary_gdf, cell_size)

    # 在边界外接矩形上铺设 fishnet
    minx, miny, maxx, maxy = boundary_gdf.total_bounds
    cells, x = [], minx
    while x < maxx:
        y = miny
        while y < maxy:
            cells.append(box(x, y, x + cell_size, y + cell_size))
            y += cell_size
        x += cell_size

    return _clip_and_index(cells, boundary_gdf.crs, boundary_gdf, clip)


def create_hexagonal_grid(boundary_gdf, cell_size, clip=True):
    """Build a pointy-top hexagonal grid covering a boundary polygon.

    Hexagons tile the plane with six equidistant neighbours and approximate a
    circle better than squares, so they sample a continuous surface more
    isotropically (no axis-vs-diagonal direction bias). They are well suited to
    interpolation surfaces and neighbourhood analysis. (For population weighting
    against a *square* census grid, prefer :func:`create_regular_grid`, whose
    cells align 1:1 with the census cells.)

    Parameters
    ----------
    boundary_gdf : GeoDataFrame  研究区边界，必须是投影坐标系
    cell_size : float            六边形外接圆半径 R（中心到顶点，CRS 单位/米）
    clip : bool                  True 时只保留与边界相交的整个六边形

    Returns
    -------
    GeoDataFrame  含 'grid_id' 列，CRS 与输入一致
    """
    _validate_projected_boundary(boundary_gdf, cell_size)

    r = cell_size                      # 外接圆半径（中心 -> 顶点）
    dx = math.sqrt(3) * r              # 同一行相邻中心的水平间距 (= 对边宽)
    dy = 1.5 * r                       # 相邻行的垂直间距
    # pointy-top 六边形顶点：从 30° 起每隔 60° 一个顶点
    offsets = [(r * math.cos(math.radians(30 + 60 * k)),
                r * math.sin(math.radians(30 + 60 * k))) for k in range(6)]

    minx, miny, maxx, maxy = boundary_gdf.total_bounds
    cells = []
    row = 0
    y = miny - r
    while y <= maxy + r:
        x_shift = dx / 2 if (row % 2) else 0.0      # 奇数行右移半格，互相嵌合
        x = minx - r + x_shift
        while x <= maxx + r:
            cells.append(Polygon([(x + ox, y + oy) for ox, oy in offsets]))
            x += dx
        y += dy
        row += 1

    return _clip_and_index(cells, boundary_gdf.crs, boundary_gdf, clip)

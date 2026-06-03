# -*- coding: utf-8 -*-
"""Regular grid (fishnet) generation with CRS validation."""
import geopandas as gpd
from shapely.geometry import box


def create_regular_grid(boundary_gdf, cell_size, clip=True):
    """Build a regular square grid (fishnet) covering a boundary polygon.

    Parameters
    ----------
    boundary_gdf : GeoDataFrame  研究区边界，必须是投影坐标系
    cell_size : float            网格边长（CRS 单位，UTM 下即米）
    clip : bool                  True 时只保留与边界相交的网格（整格保留，不切割）

    Returns
    -------
    GeoDataFrame  含 'grid_id' 列，CRS 与输入一致
    """
    # 1) CRS 校验：缺失或地理坐标系都拒绝
    if boundary_gdf.crs is None:
        raise ValueError("Boundary has no CRS defined.")
    if boundary_gdf.crs.is_geographic:
        raise ValueError("Use a projected CRS (e.g. EPSG:32632); degrees distort distance/area.")
    if cell_size <= 0:
        raise ValueError("cell_size must be positive.")

    # 2) 在边界外接矩形上铺设 fishnet
    minx, miny, maxx, maxy = boundary_gdf.total_bounds
    cells, x = [], minx
    while x < maxx:
        y = miny
        while y < maxy:
            cells.append(box(x, y, x + cell_size, y + cell_size))
            y += cell_size
        x += cell_size
    grid = gpd.GeoDataFrame(geometry=cells, crs=boundary_gdf.crs)

    # 3) 只保留与边界相交的整格（不切割几何）
    if clip:
        poly = boundary_gdf.union_all() if hasattr(boundary_gdf, "union_all") else boundary_gdf.unary_union
        grid = grid[grid.intersects(poly)].copy()

    # 4) 重排干净的整数 id
    grid["grid_id"] = range(len(grid))
    return grid.reset_index(drop=True)

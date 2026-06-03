# -*- coding: utf-8 -*-
"""Inverse Distance Weighting (IDW) interpolation from points to grid centroids."""
import numpy as np


def idw_interpolation(points_gdf, grid_gdf, value_col, power=2, max_distance=None):
    """把监测点观测值通过 IDW 插值到网格质心。

    Parameters
    ----------
    points_gdf : GeoDataFrame   监测点（含观测值列），投影坐标系
    grid_gdf   : GeoDataFrame   目标网格（多边形）
    value_col  : str            points_gdf 中要插值的数值列名
    power      : float          距离衰减指数 p，w = 1 / d**p
    max_distance : float | None 只用该距离内的点，None 表示用全部点

    Returns
    -------
    GeoDataFrame  grid_gdf 的副本，新增 'idw_value' 列
    """
    # 输入校验（沿用课上讲的 assert 风格做输入守卫）
    assert points_gdf.crs == grid_gdf.crs, "points and grid must share the same CRS"
    assert value_col in points_gdf.columns, f"'{value_col}' not in points_gdf"

    out = grid_gdf.copy()
    centroids = out.geometry.centroid

    pts = np.array([(g.x, g.y) for g in points_gdf.geometry])
    vals = points_gdf[value_col].to_numpy(dtype=float)
    targets = np.array([(c.x, c.y) for c in centroids])

    results = []
    for tx, ty in targets:
        # 每个质心到所有站点的距离：numpy 广播向量化
        d = np.sqrt((pts[:, 0] - tx) ** 2 + (pts[:, 1] - ty) ** 2)

        # 奇异点：质心几乎落在站点上 -> 直接取该站点值，避免除零
        coincident = d < 1e-6
        if coincident.any():
            results.append(vals[coincident][0])
            continue

        # 可选最大距离过滤（局部 IDW）
        if max_distance is not None:
            m = d <= max_distance
            d, v = d[m], vals[m]
        else:
            v = vals
        if d.size == 0:
            results.append(np.nan)
            continue

        # IDW 核心：w = 1/d^p, value = Σ(w·v) / Σw
        w = 1.0 / (d ** power)
        results.append(np.sum(w * v) / np.sum(w))

    out["idw_value"] = results
    return out

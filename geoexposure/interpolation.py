# -*- coding: utf-8 -*-
"""Inverse Distance Weighting (IDW) interpolation from points to grid centroids."""
import numpy as np


def idw_interpolation(points_gdf, grid_gdf, value_col, power=2, max_distance=None):
    """Interpolate point observations onto grid centroids using IDW.

    Parameters
    ----------
    points_gdf : GeoDataFrame
        Measurement points (carrying the value column); projected CRS.
    grid_gdf : GeoDataFrame
        Target polygon grid.
    value_col : str
        Column in ``points_gdf`` to interpolate.
    power : float
        Distance-decay exponent p, where w = 1 / d**p.
    max_distance : float or None
        Use only points within this distance; None uses all points.

    Returns
    -------
    GeoDataFrame
        A copy of ``grid_gdf`` with a new ``idw_value`` column.
    """
    # Input guards (assert-style validation as taught in the course).
    assert points_gdf.crs == grid_gdf.crs, "points and grid must share the same CRS"
    assert value_col in points_gdf.columns, f"'{value_col}' not in points_gdf"

    out = grid_gdf.copy()
    centroids = out.geometry.centroid

    pts = np.array([(g.x, g.y) for g in points_gdf.geometry])
    vals = points_gdf[value_col].to_numpy(dtype=float)
    targets = np.array([(c.x, c.y) for c in centroids])

    results = []
    for tx, ty in targets:
        # Distance from this centroid to every station (vectorised over stations).
        d = np.sqrt((pts[:, 0] - tx) ** 2 + (pts[:, 1] - ty) ** 2)

        # Singularity: centroid (almost) on a station -> take that value, avoid div-by-zero.
        coincident = d < 1e-6
        if coincident.any():
            results.append(vals[coincident][0])
            continue

        # Optional maximum-distance filter (local IDW).
        if max_distance is not None:
            m = d <= max_distance
            d, v = d[m], vals[m]
        else:
            v = vals
        if d.size == 0:
            results.append(np.nan)
            continue

        # IDW core: w = 1/d^p, value = sum(w*v) / sum(w).
        w = 1.0 / (d ** power)
        results.append(np.sum(w * v) / np.sum(w))

    out["idw_value"] = results
    return out

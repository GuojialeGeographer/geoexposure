"""Inverse-distance-weighted (IDW) interpolation from points to a grid."""

from __future__ import annotations

import geopandas as gpd


def idw_interpolation(points_gdf: gpd.GeoDataFrame, grid_gdf: gpd.GeoDataFrame,
                      value_col: str, power: float = 2,
                      max_distance: float | None = None) -> gpd.GeoDataFrame:
    """Interpolate point values onto grid cells using IDW.

    Parameters
    ----------
    points_gdf : GeoDataFrame
        Measurement points carrying ``value_col`` (e.g. ``no2``).
    grid_gdf : GeoDataFrame
        Target grid (e.g. from :func:`create_regular_grid`).
    value_col : str
        Column in ``points_gdf`` holding the value to interpolate.
    power : float, default 2
        IDW power parameter (higher = more local).
    max_distance : float or None, default None
        Optional cutoff distance; points beyond it are ignored.

    Returns
    -------
    GeoDataFrame
        Copy of ``grid_gdf`` with a new ``idw_value`` column.
    """
    raise NotImplementedError("Implemented in Step 3.")

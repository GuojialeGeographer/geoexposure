"""Regular grid generation over a study-area boundary."""

from __future__ import annotations

import geopandas as gpd


def create_regular_grid(boundary_gdf: gpd.GeoDataFrame, cell_size: float,
                        clip: bool = True) -> gpd.GeoDataFrame:
    """Build a regular square grid covering a boundary.

    Parameters
    ----------
    boundary_gdf : GeoDataFrame
        Study-area boundary. Must be in a projected CRS (EPSG:32632).
    cell_size : float
        Edge length of each square cell, in CRS units (metres).
    clip : bool, default True
        If True, keep only cells intersecting the boundary.

    Returns
    -------
    GeoDataFrame
        Grid cells with a ``grid_id`` column, in the boundary CRS.
    """
    raise NotImplementedError("Implemented in Step 2.")

"""Exposure inequality / environmental-justice summary."""

from __future__ import annotations

import geopandas as gpd


def exposure_inequality_summary(grid_gdf: gpd.GeoDataFrame, exposure_col: str,
                                population_col: str,
                                quantile: float = 0.25) -> dict:
    """Summarise exposure inequality between high- and low-exposure cells.

    Parameters
    ----------
    grid_gdf : GeoDataFrame
        Grid carrying both concentration and population columns.
    exposure_col : str
        Concentration column (e.g. ``idw_value``).
    population_col : str
        Population column (e.g. ``population``).
    quantile : float, default 0.25
        Tail fraction defining the "high" (top) and "low" (bottom) groups.

    Returns
    -------
    dict
        Keys: ``high_exposure_mean``, ``low_exposure_mean``, ``ratio``,
        ``pop_share_high``.
    """
    raise NotImplementedError("Implemented in Step 5.")

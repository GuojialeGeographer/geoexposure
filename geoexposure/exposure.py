"""Population-weighted exposure metrics.

A grid cell carries a *concentration* (``idw_value``). Only once it is
aggregated with population does the scalar become an *exposure*.
"""

from __future__ import annotations

import geopandas as gpd


def population_weighted_exposure(grid_gdf: gpd.GeoDataFrame, exposure_col: str,
                                 population_col: str) -> float:
    """Population-weighted mean concentration (the PWE scalar).

    PWE = sum(value_i * pop_i) / sum(pop_i)
    """
    raise NotImplementedError("Implemented in Step 4.")


def area_weighted_mean(grid_gdf: gpd.GeoDataFrame, exposure_col: str) -> float:
    """Plain (area-weighted) mean concentration across all cells."""
    raise NotImplementedError("Implemented in Step 4.")


def exposure_bias(pwe: float, mean_value: float) -> float:
    """Percentage bias of population-weighted vs. area-weighted mean.

    bias(%) = 100 * (pwe - mean_value) / mean_value
    """
    raise NotImplementedError("Implemented in Step 4.")

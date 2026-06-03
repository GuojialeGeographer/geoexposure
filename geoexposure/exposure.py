# -*- coding: utf-8 -*-
"""Population-weighted exposure metrics.

A grid cell carries a *concentration* (``idw_value``). Only once it is
aggregated with population does the scalar become an *exposure*.
"""


def population_weighted_exposure(grid_gdf, exposure_col, population_col):
    """Population-weighted exposure (PWE) -- "what the average person breathes".

        PWE = sum(c_i * p_i) / sum(p_i)

    Each cell concentration c_i is weighted by its population p_i, so more
    populated cells count more.

    Parameters
    ----------
    grid_gdf : GeoDataFrame
        Grid carrying both the concentration and population columns.
    exposure_col : str
        Concentration column (e.g. 'idw_value').
    population_col : str
        Population column (e.g. 'population').

    Returns
    -------
    float
        Population-weighted mean concentration.
    """
    assert exposure_col in grid_gdf.columns, f"'{exposure_col}' not in grid"
    assert population_col in grid_gdf.columns, f"'{population_col}' not in grid"
    pop = grid_gdf[population_col]
    assert (pop >= 0).all(), "population must be non-negative"
    total_pop = pop.sum()
    assert total_pop > 0, "total population must be > 0 (avoid divide-by-zero)"
    return float((grid_gdf[exposure_col] * pop).sum() / total_pop)


def area_weighted_mean(grid_gdf, exposure_col):
    """Spatial (area-weighted) mean -- "how polluted the average cell is".

        AM = sum(c_i * a_i) / sum(a_i)        a_i = cell area (geometry.area)

    Treats empty and densely populated cells alike. With equal-area cells it
    reduces to the arithmetic mean.

    Parameters
    ----------
    grid_gdf : GeoDataFrame
        Grid carrying the concentration column.
    exposure_col : str
        Concentration column.

    Returns
    -------
    float
        Area-weighted mean concentration.
    """
    assert exposure_col in grid_gdf.columns, f"'{exposure_col}' not in grid"
    area = grid_gdf.geometry.area
    total_area = area.sum()
    assert total_area > 0, "total area must be > 0"
    return float((grid_gdf[exposure_col] * area).sum() / total_area)


def exposure_bias(pwe, mean_value):
    """Percentage bias of population-weighted vs. spatial mean.

        bias% = (pwe - mean_value) / mean_value * 100

    When pollution and population are positively correlated, pwe > spatial mean
    and the bias is positive: a plain pollution-map average *underestimates*
    real human exposure. This is the rationale (and policy meaning) of
    population weighting.

    Parameters
    ----------
    pwe : float
        Population-weighted exposure.
    mean_value : float
        Spatial (area-weighted) mean.

    Returns
    -------
    float
        Percentage bias.
    """
    assert mean_value != 0, "mean_value must be non-zero (avoid divide-by-zero)"
    return float((pwe - mean_value) / mean_value * 100.0)

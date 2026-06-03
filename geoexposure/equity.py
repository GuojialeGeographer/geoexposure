# -*- coding: utf-8 -*-
"""Exposure inequality / environmental-justice summary."""


def exposure_inequality_summary(grid_gdf, exposure_col, population_col,
                                quantile=0.25):
    """Compare exposure inequality between high- and low-exposure areas.

    Cells are split by concentration into a "high-exposure" group (top
    ``quantile`` fraction) and a "low-exposure" group (bottom ``quantile``
    fraction). The function compares the population-weighted mean exposure of
    the two groups and reports the population share living in the high group.

    Parameters
    ----------
    grid_gdf : GeoDataFrame
        Grid carrying both the concentration and population columns.
    exposure_col : str
        Concentration column (e.g. 'idw_value').
    population_col : str
        Population column (e.g. 'population').
    quantile : float
        Tail fraction defining the high/low groups (default 0.25).

    Returns
    -------
    dict
        {high_exposure_mean, low_exposure_mean, ratio, pop_share_high}
            high_exposure_mean : population-weighted mean of the high group
            low_exposure_mean  : population-weighted mean of the low group
            ratio              : high / low (> 1 indicates inequality)
            pop_share_high     : population in the high group / total population
    """
    assert exposure_col in grid_gdf.columns, f"'{exposure_col}' not in grid"
    assert population_col in grid_gdf.columns, f"'{population_col}' not in grid"
    assert 0 < quantile < 0.5, "quantile must be in (0, 0.5)"

    c = grid_gdf[exposure_col]
    pop = grid_gdf[population_col]
    assert (pop >= 0).all(), "population must be non-negative"
    total_pop = pop.sum()
    assert total_pop > 0, "total population must be > 0"

    hi_thr = c.quantile(1 - quantile)   # high-exposure threshold (upper quantile)
    lo_thr = c.quantile(quantile)       # low-exposure threshold (lower quantile)
    high = grid_gdf[c >= hi_thr]
    low = grid_gdf[c <= lo_thr]

    def _pop_weighted_mean(sub):
        """Population-weighted mean exposure of a subset of cells."""
        p = sub[population_col].sum()
        if p > 0:
            return float((sub[exposure_col] * sub[population_col]).sum() / p)
        return float(sub[exposure_col].mean())   # fall back to arithmetic mean if no population

    high_mean = _pop_weighted_mean(high)
    low_mean = _pop_weighted_mean(low)
    ratio = float(high_mean / low_mean) if low_mean != 0 else float("inf")
    pop_share_high = float(high[population_col].sum() / total_pop)

    return {
        "high_exposure_mean": high_mean,
        "low_exposure_mean": low_mean,
        "ratio": ratio,
        "pop_share_high": pop_share_high,
    }

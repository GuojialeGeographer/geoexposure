# -*- coding: utf-8 -*-
"""Population-weighted exposure metrics.

A grid cell carries a *concentration* (``idw_value``). Only once it is
aggregated with population does the scalar become an *exposure*.
"""


def population_weighted_exposure(grid_gdf, exposure_col, population_col):
    """人口加权暴露 (PWE) —— "平均一个人暴露在多高的污染下"。

        PWE = Σ(cᵢ · pᵢ) / Σ(pᵢ)

    每个格子的浓度 cᵢ 按它的人口 pᵢ 加权：人多的地方权重大。

    Parameters
    ----------
    grid_gdf : GeoDataFrame   含浓度列与人口列的网格
    exposure_col : str        浓度列名（如 'idw_value'）
    population_col : str       人口列名（如 'population'）

    Returns
    -------
    float  人口加权平均浓度
    """
    assert exposure_col in grid_gdf.columns, f"'{exposure_col}' not in grid"
    assert population_col in grid_gdf.columns, f"'{population_col}' not in grid"
    pop = grid_gdf[population_col]
    assert (pop >= 0).all(), "population must be non-negative"
    total_pop = pop.sum()
    assert total_pop > 0, "total population must be > 0 (avoid divide-by-zero)"
    return float((grid_gdf[exposure_col] * pop).sum() / total_pop)


def area_weighted_mean(grid_gdf, exposure_col):
    """空间(面积加权)均值 —— "平均一个格子里污染多高"。

        AM = Σ(cᵢ · aᵢ) / Σ(aᵢ)        aᵢ = 格子面积 geometry.area

    把空旷格子和人口密集格子一视同仁。整格等面积时退化成算术平均。

    Parameters
    ----------
    grid_gdf : GeoDataFrame   含浓度列的网格
    exposure_col : str        浓度列名

    Returns
    -------
    float  面积加权平均浓度
    """
    assert exposure_col in grid_gdf.columns, f"'{exposure_col}' not in grid"
    area = grid_gdf.geometry.area
    total_area = area.sum()
    assert total_area > 0, "total area must be > 0"
    return float((grid_gdf[exposure_col] * area).sum() / total_area)


def exposure_bias(pwe, mean_value):
    """人口加权 vs 空间均值的百分比偏倚。

        bias% = (pwe − mean_value) / mean_value × 100

    污染与人口正相关时 pwe > 空间均值，bias 为正：单看污染地图的均值
    会"低估"真实的人群暴露。这就是做人口加权的理由与政策含义。

    Parameters
    ----------
    pwe : float          人口加权暴露
    mean_value : float   空间(面积加权)均值

    Returns
    -------
    float  百分比偏倚
    """
    assert mean_value != 0, "mean_value must be non-zero (avoid divide-by-zero)"
    return float((pwe - mean_value) / mean_value * 100.0)

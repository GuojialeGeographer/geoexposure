# -*- coding: utf-8 -*-
"""Exposure inequality / environmental-justice summary."""


def exposure_inequality_summary(grid_gdf, exposure_col, population_col,
                                quantile=0.25):
    """比较高暴露区与低暴露区之间的暴露不平等。

    按浓度把网格分成"高暴露"(顶部 quantile 分位)与"低暴露"(底部 quantile
    分位)两组，比较两组的人口加权平均暴露，并报告住在高暴露区的人口占比。

    Parameters
    ----------
    grid_gdf : GeoDataFrame   含浓度列与人口列的网格
    exposure_col : str        浓度列名（如 'idw_value'）
    population_col : str       人口列名（如 'population'）
    quantile : float          尾部比例，定义高/低分组（默认 0.25）

    Returns
    -------
    dict  {high_exposure_mean, low_exposure_mean, ratio, pop_share_high}
        high_exposure_mean : 高暴露组的人口加权平均浓度
        low_exposure_mean  : 低暴露组的人口加权平均浓度
        ratio              : 高/低 比值（>1 表示存在不平等）
        pop_share_high     : 住在高暴露组的人口占总人口的比例
    """
    assert exposure_col in grid_gdf.columns, f"'{exposure_col}' not in grid"
    assert population_col in grid_gdf.columns, f"'{population_col}' not in grid"
    assert 0 < quantile < 0.5, "quantile must be in (0, 0.5)"

    c = grid_gdf[exposure_col]
    pop = grid_gdf[population_col]
    assert (pop >= 0).all(), "population must be non-negative"
    total_pop = pop.sum()
    assert total_pop > 0, "total population must be > 0"

    hi_thr = c.quantile(1 - quantile)   # 高暴露阈值（上分位）
    lo_thr = c.quantile(quantile)       # 低暴露阈值（下分位）
    high = grid_gdf[c >= hi_thr]
    low = grid_gdf[c <= lo_thr]

    def _pop_weighted_mean(sub):
        p = sub[population_col].sum()
        if p > 0:
            return float((sub[exposure_col] * sub[population_col]).sum() / p)
        return float(sub[exposure_col].mean())   # 该组无人口时退回算术平均

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

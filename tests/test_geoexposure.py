# -*- coding: utf-8 -*-
"""Unit tests for geoexposure.

The exposure tests use a hand-computed two-cell case so the expected numbers
can be verified by hand; the spatial tests assert mathematical properties
(bounds, counts, CRS) rather than exact data values.
"""

import geopandas as gpd
import pytest
from shapely.geometry import box, Point

import geoexposure as gx
from geoexposure.grid import create_regular_grid
from geoexposure.interpolation import idw_interpolation
from geoexposure.exposure import (
    population_weighted_exposure, area_weighted_mean, exposure_bias,
)
from geoexposure.equity import exposure_inequality_summary

CRS = "EPSG:32632"


@pytest.fixture
def two_cell_grid():
    """Two equal 500 m cells. PWE = 30, area mean = 25, bias = +20%."""
    return gpd.GeoDataFrame(
        {"idw_value": [15.0, 35.0], "population": [100, 300]},
        geometry=[box(0, 0, 500, 500), box(500, 0, 1000, 500)],
        crs=CRS,
    )


# ---- package ----
def test_version_and_public_api():
    assert gx.__version__ == "0.1.0"
    for name in gx.__all__:
        assert hasattr(gx, name)


# ---- grid ----
def test_grid_count_crs_and_ids():
    b = gpd.GeoDataFrame(geometry=[box(512000, 5032000, 516000, 5036000)], crs=CRS)
    grid = create_regular_grid(b, 500)
    assert len(grid) == 64                       # 4km / 500m = 8x8
    assert grid.crs == b.crs
    assert grid["grid_id"].tolist() == list(range(64))


def test_grid_rejects_geographic_crs():
    b = gpd.GeoDataFrame(geometry=[box(512000, 5032000, 516000, 5036000)], crs=CRS).to_crs(4326)
    with pytest.raises(ValueError):
        create_regular_grid(b, 0.005)


def test_grid_rejects_nonpositive_cell_size():
    b = gpd.GeoDataFrame(geometry=[box(0, 0, 1000, 1000)], crs=CRS)
    with pytest.raises(ValueError):
        create_regular_grid(b, 0)


# ---- interpolation (IDW) ----
def test_idw_stays_within_input_bounds():
    b = gpd.GeoDataFrame(geometry=[box(512000, 5032000, 516000, 5036000)], crs=CRS)
    grid = create_regular_grid(b, 500)
    pts = gpd.GeoDataFrame(
        {"no2": [44.0, 16.0, 16.0, 16.0, 16.0]},
        geometry=[Point(514000, 5034000), Point(512200, 5032200),
                  Point(515800, 5032200), Point(512200, 5035800),
                  Point(515800, 5035800)],
        crs=CRS,
    )
    out = idw_interpolation(pts, grid, "no2", power=2)
    assert "idw_value" in out.columns
    assert out["idw_value"].min() >= 16 - 1e-9
    assert out["idw_value"].max() <= 44 + 1e-9


def test_idw_returns_station_value_when_coincident():
    cell = gpd.GeoDataFrame(geometry=[box(0, 0, 1000, 1000)], crs=CRS)
    grid = create_regular_grid(cell, 1000)        # single cell, centroid (500, 500)
    pts = gpd.GeoDataFrame(
        {"no2": [42.0, 10.0]},
        geometry=[Point(500, 500), Point(0, 0)], crs=CRS,
    )
    out = idw_interpolation(pts, grid, "no2")
    assert out["idw_value"].iloc[0] == pytest.approx(42.0)


def test_idw_rejects_crs_mismatch():
    b = gpd.GeoDataFrame(geometry=[box(512000, 5032000, 516000, 5036000)], crs=CRS)
    grid = create_regular_grid(b, 1000)
    pts = gpd.GeoDataFrame({"no2": [20.0]}, geometry=[Point(514000, 5034000)], crs=CRS)
    with pytest.raises(AssertionError):
        idw_interpolation(pts.to_crs(4326), grid, "no2")


# ---- exposure (the core; hand-computed) ----
def test_pwe_hand_computed(two_cell_grid):
    # (15*100 + 35*300) / 400 = 30
    assert population_weighted_exposure(two_cell_grid, "idw_value", "population") == pytest.approx(30.0)


def test_area_weighted_mean_hand_computed(two_cell_grid):
    # equal areas -> (15 + 35) / 2 = 25
    assert area_weighted_mean(two_cell_grid, "idw_value") == pytest.approx(25.0)


def test_exposure_bias_hand_computed():
    # (30 - 25) / 25 * 100 = 20
    assert exposure_bias(30.0, 25.0) == pytest.approx(20.0)


def test_pwe_rejects_missing_column(two_cell_grid):
    with pytest.raises(AssertionError):
        population_weighted_exposure(two_cell_grid, "does_not_exist", "population")


def test_pwe_rejects_zero_total_population():
    g = gpd.GeoDataFrame(
        {"idw_value": [10.0, 20.0], "population": [0, 0]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1)], crs=CRS,
    )
    with pytest.raises(AssertionError):
        population_weighted_exposure(g, "idw_value", "population")


def test_exposure_bias_rejects_zero_mean():
    with pytest.raises(AssertionError):
        exposure_bias(10.0, 0.0)


# ---- equity ----
def test_equity_summary_structure_and_ordering():
    g = gpd.GeoDataFrame(
        {"idw_value": [10.0, 20.0, 30.0, 40.0], "population": [100, 100, 100, 700]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(2, 0, 3, 1), box(3, 0, 4, 1)],
        crs=CRS,
    )
    s = exposure_inequality_summary(g, "idw_value", "population", quantile=0.25)
    assert set(s) == {"high_exposure_mean", "low_exposure_mean", "ratio", "pop_share_high"}
    assert s["high_exposure_mean"] > s["low_exposure_mean"]
    assert s["ratio"] > 1
    assert 0.0 <= s["pop_share_high"] <= 1.0

"""geoexposure: point-to-population environmental exposure toolkit.

A small, focused geospatial processing chain:
    points -> regular grid -> IDW interpolation -> population-weighted
    exposure -> equity / inequality summary.

All spatial data is expected in EPSG:32632 (UTM zone 32N, Milan).
"""

from .grid import create_regular_grid, create_hexagonal_grid
from .interpolation import idw_interpolation
from .exposure import (
    population_weighted_exposure,
    area_weighted_mean,
    exposure_bias,
)
from .equity import exposure_inequality_summary
from .io import load_sample_data
from .plotting import plot_choropleth

__version__ = "0.1.0"

__all__ = [
    "create_regular_grid",
    "create_hexagonal_grid",
    "idw_interpolation",
    "population_weighted_exposure",
    "area_weighted_mean",
    "exposure_bias",
    "exposure_inequality_summary",
    "load_sample_data",
    "plot_choropleth",
]

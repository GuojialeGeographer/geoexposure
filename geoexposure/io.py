# -*- coding: utf-8 -*-
"""Loading of the bundled Milan sample data.

The files under ``data/`` are real Milan data in EPSG:32632: an ISTAT
administrative boundary, ARPA Lombardia NO2 monitoring stations, and the ISTAT
2021 census population on a 500 m grid (see ``data/README.md`` for provenance).
Replace the three GeoJSON files (same filenames, columns and CRS) to run the
analysis on different data.
"""

from pathlib import Path

import geopandas as gpd

_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
_TARGET_EPSG = 32632
_FILES = {
    "boundary": "boundary.geojson",
    "stations": "stations.geojson",            # carries 'no2'
    "population_grid": "population_grid.geojson",  # carries 'population'
}


def load_sample_data(data_dir=None):
    """Load the bundled Milan sample datasets.

    Parameters
    ----------
    data_dir : str or Path, optional
        Override the directory to read from (defaults to the package ``data/``).

    Returns
    -------
    dict
        Keys ``boundary``, ``stations``, ``population_grid``, each a
        GeoDataFrame reprojected to EPSG:32632. Stations carry a ``no2``
        column; the population grid carries a ``population`` column.
    """
    base = Path(data_dir) if data_dir is not None else _DATA_DIR
    out = {}
    for key, fname in _FILES.items():
        path = base / fname
        if not path.exists():
            raise FileNotFoundError(f"Sample data file not found: {path}")
        gdf = gpd.read_file(path)
        if gdf.crs is None:
            raise ValueError(f"{fname} has no CRS; expected EPSG:{_TARGET_EPSG}")
        if gdf.crs.to_epsg() != _TARGET_EPSG:
            gdf = gdf.to_crs(epsg=_TARGET_EPSG)
        out[key] = gdf
    return out

"""Loading of the bundled real-world Milan sample data."""

from __future__ import annotations


def load_sample_data() -> dict:
    """Load the bundled Milan sample datasets.

    Returns
    -------
    dict
        Keys ``boundary``, ``stations``, ``population_grid``, each a
        GeoDataFrame in EPSG:32632. Stations carry a ``no2`` column;
        the population grid carries a ``population`` column.
    """
    raise NotImplementedError("Implemented in Step 6.")

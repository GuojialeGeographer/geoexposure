"""End-to-end example: points -> grid -> IDW -> exposure -> equity.

Fleshed out in Step 8 once the modules are implemented.
"""

from geoexposure import (
    load_sample_data,
    create_regular_grid,
    idw_interpolation,
    population_weighted_exposure,
    area_weighted_mean,
    exposure_bias,
    exposure_inequality_summary,
)


def main() -> None:
    data = load_sample_data()
    grid = create_regular_grid(data["boundary"], cell_size=500)
    grid = idw_interpolation(data["stations"], grid, value_col="no2")
    # ... join population, then compute metrics ...
    raise NotImplementedError("Completed in Step 8.")


if __name__ == "__main__":
    main()

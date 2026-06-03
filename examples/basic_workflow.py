# -*- coding: utf-8 -*-
"""End-to-end example: points -> grid -> IDW -> exposure -> equity.

Run with:  python examples/basic_workflow.py
"""

import geopandas as gpd

from geoexposure import (
    load_sample_data,
    create_regular_grid,
    idw_interpolation,
    population_weighted_exposure,
    area_weighted_mean,
    exposure_bias,
    exposure_inequality_summary,
)


def main():
    # 1) Load the bundled Milan sample data (all EPSG:32632).
    data = load_sample_data()
    boundary, stations, pop = data["boundary"], data["stations"], data["population_grid"]

    # 2) Build a regular analysis grid over the study area.
    #    500 m matches the census population grid, so each analysis cell maps
    #    cleanly to one population cell (full population coverage, no undercount).
    grid = create_regular_grid(boundary, cell_size=500)

    # 3) Interpolate the station NO2 values onto the grid centroids (IDW).
    grid = idw_interpolation(stations, grid, value_col="no2", power=2)

    # 4) Attach population: each cell takes the population of the population
    #    polygon that contains its centroid (a simple spatial join).
    centroids = grid.copy()
    centroids["geometry"] = grid.geometry.centroid
    joined = gpd.sjoin(centroids, pop[["population", "geometry"]],
                       predicate="within", how="left")
    grid["population"] = joined["population"].fillna(0.0).to_numpy()

    # 5) Exposure metrics.
    pwe = population_weighted_exposure(grid, "idw_value", "population")
    awm = area_weighted_mean(grid, "idw_value")
    bias = exposure_bias(pwe, awm)

    # 6) Equity summary.
    eq = exposure_inequality_summary(grid, "idw_value", "population", quantile=0.25)

    print(f"Grid cells:                 {len(grid)}")
    print(f"Population-weighted exposure: {pwe:.2f} ug/m3")
    print(f"Area-weighted mean:          {awm:.2f} ug/m3")
    print(f"Exposure bias:               {bias:+.1f} %")
    print("Equity summary:")
    print(f"  high-exposure mean: {eq['high_exposure_mean']:.2f}")
    print(f"  low-exposure mean:  {eq['low_exposure_mean']:.2f}")
    print(f"  ratio (high/low):   {eq['ratio']:.2f}")
    print(f"  pop share in high:  {eq['pop_share_high']:.1%}")


if __name__ == "__main__":
    main()

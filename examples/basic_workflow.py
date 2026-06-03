# -*- coding: utf-8 -*-
"""End-to-end example: points -> grid -> IDW -> exposure -> equity -> outputs.

Runs the full geoexposure chain on the real Milan sample data and writes three
kinds of output to ``outputs/``:
  * data   : the enriched analysis grid as GeoJSON
  * table  : the metrics + equity summary as CSV (also printed)
  * charts : two PNG maps (NO2 surface with stations; exposure groups)

Run with:  python examples/basic_workflow.py
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from geoexposure import (
    load_sample_data,
    create_regular_grid,
    idw_interpolation,
    population_weighted_exposure,
    area_weighted_mean,
    exposure_bias,
    exposure_inequality_summary,
    plot_choropleth,
)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"


def attach_population(grid, population_gdf, population_col="population"):
    """Sum each census cell's population into the analysis cell that contains
    its centroid. Works for any analysis-grid shape (square or hexagonal) and
    keeps full population coverage."""
    census = population_gdf.copy()
    census["geometry"] = population_gdf.geometry.centroid
    joined = gpd.sjoin(census[[population_col, "geometry"]],
                       grid[["grid_id", "geometry"]], predicate="within", how="left")
    pop_by_cell = joined.groupby("grid_id")[population_col].sum()
    grid = grid.copy()
    grid["population"] = grid["grid_id"].map(pop_by_cell).fillna(0.0)
    return grid


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1) Load real Milan data (EPSG:32632).
    data = load_sample_data()
    boundary, stations, pop = data["boundary"], data["stations"], data["population_grid"]

    # 2) Square analysis grid (500 m matches the census grid 1:1).
    grid = create_regular_grid(boundary, cell_size=500)

    # 3) IDW the station NO2 onto the grid centroids.
    grid = idw_interpolation(stations, grid, value_col="no2", power=2)

    # 4) Attach population.
    grid = attach_population(grid, pop)

    # 5) Exposure metrics.
    pwe = population_weighted_exposure(grid, "idw_value", "population")
    awm = area_weighted_mean(grid, "idw_value")
    bias = exposure_bias(pwe, awm)

    # 6) Equity summary.
    eq = exposure_inequality_summary(grid, "idw_value", "population", quantile=0.25)

    # --- TABLE output: tidy metrics table -> print + CSV ---
    summary = pd.DataFrame(
        {"metric": ["grid_cells", "population_total", "population_weighted_exposure",
                    "area_weighted_mean", "exposure_bias_pct", "high_exposure_mean",
                    "low_exposure_mean", "inequality_ratio", "pop_share_high"],
         "value": [len(grid), grid["population"].sum(), pwe, awm, bias,
                   eq["high_exposure_mean"], eq["low_exposure_mean"],
                   eq["ratio"], eq["pop_share_high"]]}
    )
    summary["value"] = summary["value"].round(2)
    print(summary.to_string(index=False))
    summary.to_csv(OUTPUT_DIR / "summary.csv", index=False)

    # --- DATA output: enriched grid as GeoJSON ---
    grid.to_file(OUTPUT_DIR / "grid_no2_exposure.geojson", driver="GeoJSON")

    # --- CHART output 1: NO2 IDW surface with monitoring stations ---
    ax = plot_choropleth(grid, "idw_value", cmap="YlOrRd", points_gdf=stations,
                         title="Milan NO2 IDW surface (ug/m3) + ARPA stations",
                         savepath=OUTPUT_DIR / "map_no2_idw.png")
    plt.close(ax.figure)

    # --- CHART output 2: high vs low exposure groups ---
    hi = grid["idw_value"].quantile(0.75)
    lo = grid["idw_value"].quantile(0.25)
    grid["exposure_group"] = 1                      # middle
    grid.loc[grid["idw_value"] >= hi, "exposure_group"] = 2   # high
    grid.loc[grid["idw_value"] <= lo, "exposure_group"] = 0   # low
    ax = plot_choropleth(grid, "exposure_group", cmap="RdYlGn_r",
                         title="Exposure groups (0=low, 1=mid, 2=high)",
                         savepath=OUTPUT_DIR / "map_exposure_groups.png")
    plt.close(ax.figure)

    print(f"\nOutputs written to: {OUTPUT_DIR}")
    for f in ["summary.csv", "grid_no2_exposure.geojson",
              "map_no2_idw.png", "map_exposure_groups.png"]:
        print(f"  - {f}")


if __name__ == "__main__":
    main()

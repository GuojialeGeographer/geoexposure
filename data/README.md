# datacopy for geoexposure

This folder collects the Milan NO2 data that are useful for the `geoexposure`
project. All generated project-ready vector files use EPSG:32632.

## Download sources

The files in this folder are derived from the thesis project's downloaded and
processed Milan datasets. The upstream download sources are:

| Data | Upstream source | Download/access route used in the thesis project | Local derived files in this folder |
|---|---|---|---|
| ARPA NO2 monitoring stations and hourly measurements | Regione Lombardia Open Data / ARPA Lombardia | Sensor data: `https://www.dati.lombardia.it/resource/nicp-bhqi.csv`; station metadata: `https://www.dati.lombardia.it/Ambiente/Stazioni-qualit-dell-aria/ib47-atvt`; portal: `https://www.dati.lombardia.it/` | `project_ready_geoexposure/stations.geojson`, `authoritative_sources/arpa_stations_annual.gpkg`, `optional_context/stations/*` |
| Milan metropolitan boundary and municipality polygons | ISTAT administrative boundaries, Com01012026 | ISTAT boundary archive page: `https://www.istat.it/it/archivio/222527`; local source package: `ISTAT_Milano_boundary_source_2026_Limiti01012026/Com01012026/Com01012026_WGS84.shp` | `project_ready_geoexposure/boundary.geojson`, `authoritative_sources/milan_metro_boundary.gpkg`, `authoritative_sources/milan_comuni.gpkg` |
| ISTAT census population | ISTAT 2021 census sections, Lombardia `R03_21` | ISTAT census portal: `https://www.istat.it/it/censimenti/popolazione-e-abitazioni`; local source package: `ISTAT_Lombardia_2021_census_sections_geometry_R03_21/SHP/R03_21_WGS84.shp` | `project_ready_geoexposure/population_grid.geojson`, `authoritative_sources/feature_matrix_500m.gpkg`, `optional_context/population/population_istat_500m.csv` |
| ISTAT 2023 demographic population update | ISTAT demographic tables, redistributed to the same 500 m grid | Derived in the thesis project from ISTAT 2023 population/demographic tables | `optional_context/population/population_istat_2023_500m.csv`, `optional_context/tables/57_istat_2023_demographic_summary.csv`, `optional_context/tables/58_demographic_pwe.csv` |
| WorldPop population sensitivity raster | WorldPop Italy 100 m population 2020 | WorldPop dataset page: `https://hub.worldpop.org/geodata/summary?id=49749`; local source file: `WorldPop_Italy_population_100m_2020_ita_ppp_2020.tif` | `optional_context/rasters/population_worldpop_500m.tif` |
| GHS-POP population comparison | European Commission JRC GHSL GHS-POP R2023A | Direct ZIP URL used by the thesis script: `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0.zip` | `optional_context/population/population_comparison.csv` |
| TROPOMI NO2 column raster | Google Earth Engine Sentinel-5P OFFL L3 NO2 | GEE collection: `COPERNICUS/S5P/OFFL/L3_NO2`; exported with `master thesis/scripts/gee_all_data.js` to Google Drive folder `GEE_Milan_NO2` | `optional_context/rasters/tropomi_no2_annual_2024.tif` |
| Sentinel-2 NDVI raster | Google Earth Engine Sentinel-2 Surface Reflectance Harmonized | GEE collection: `COPERNICUS/S2_SR_HARMONIZED`; exported with `master thesis/scripts/gee_all_data.js` to Google Drive folder `GEE_Milan_NO2` | `optional_context/rasters/ndvi_annual_2024_500m.tif` |
| ERA5 meteorology | Google Earth Engine ERA5-Land monthly aggregation | GEE collection: `ECMWF/ERA5_LAND/MONTHLY_AGGR`; exported with `master thesis/scripts/gee_all_data.js` | Included as covariates inside `authoritative_sources/feature_matrix_500m.gpkg` |
| OpenStreetMap road network | OpenStreetMap via OSMnx / Overpass API | OSMnx download using Overpass endpoints including `https://overpass.kumi.systems/api/interpreter` and `https://overpass-api.de/api/interpreter` | Road-derived covariates inside `authoritative_sources/feature_matrix_500m.gpkg` |
| DUSAF land use | Regione Lombardia DUSAF 7 land-use dataset | Local source package: `REGIONE_LOMBARDIA_DUSAF7_land_use_2021_latest_official/DUSAF7.shp` | `optional_context/maps/dusaf_land_use_grid.gpkg`, land-use fractions inside `authoritative_sources/feature_matrix_500m.gpkg` |

Important provenance note: `project_ready_geoexposure/*.geojson` are not raw
downloads. They are compact, CRS-normalized, column-normalized exports created
from the thesis project's processed outputs so that `geoexposure` can run with
real Milan data using its expected filenames and columns.

## Files used by the library

The three files the `geoexposure` library actually loads live directly in this
`data/` folder and are committed to the repository:

| File | Contents | Rows | Key column |
|---|---|---|---|
| `boundary.geojson` | ISTAT Milan metropolitan boundary | 1 | geometry only |
| `stations.geojson` | ARPA Lombardia NO2 stations (annual mean) | 16 | `no2` |
| `population_grid.geojson` | ISTAT 2021 census population, 500 m grid | 6687 | `population` |

All three are real Milan-coordinate data in EPSG:32632 (not illustrative
samples). `stations.geojson` renames the original NO2 column from `no2_annual`
to `no2`; `population_grid.geojson` keeps `grid_id`, `center_x`, `center_y`,
`population`, and `pop_density`.

## Local-only source data (not committed)

The following large folders are kept locally for provenance but are excluded
from the repository (see `.gitignore`) to keep it lean:

- `authoritative_sources/` — GeoPackage sources (boundaries, ARPA stations,
  500 m feature matrix, RF NO2 exposure assessment).
- `project_ready_geoexposure/` — the normalized exports the three committed
  files were copied from, plus `population_no2_surface_500m.geojson` (thesis RF
  NO2 surface + population on the same 500 m grid).
- `optional_context/` — monthly station data, ISTAT 2021/2023 population
  tables, rasters (WorldPop, TROPOMI, NDVI), and validation tables.

## Authoritative sources

- `authoritative_sources/milan_metro_boundary.gpkg`: one Milan metropolitan
  boundary multipolygon.
- `authoritative_sources/milan_comuni.gpkg`: 133 municipality polygons.
- `authoritative_sources/arpa_stations_annual.gpkg`: 16 ARPA station points;
  original NO2 annual column is `no2_annual`.
- `authoritative_sources/feature_matrix_500m.gpkg`: 500 m grid with population
  and covariates; population column is `population`.
- `authoritative_sources/no2_exposure_assessment.gpkg`: 500 m grid with
  population and RF-predicted NO2; annual NO2 column is `rf_no2_annual`.

## Optional context

- `optional_context/stations/`: monthly station NO2 and station covariates.
- `optional_context/population/`: ISTAT 2021/2023 population tables and source
  comparison.
- `optional_context/maps/`: RF NO2 surfaces, DUSAF clusters, and station SHAP
  outputs.
- `optional_context/tables/`: validation, PWE uncertainty, urban-core, cluster,
  and demographic exposure summaries.
- `optional_context/rasters/`: compact raster inputs for population, WorldPop,
  NDVI, and TROPOMI annual NO2.

## Notes

- `stations.geojson` renames the original station NO2 column from `no2_annual`
  to `no2` to match the `geoexposure` README.
- `population_grid.geojson` is a 500 m grid, not a synthetic sample. It keeps
  `grid_id`, `center_x`, `center_y`, `population`, and `pop_density`.
- The direct replacement files are real Milan-coordinate data, not illustrative
  values.

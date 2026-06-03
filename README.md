# geoexposure

A small Python toolkit for **point-to-population environmental exposure**.
It implements one complete geospatial processing chain:

> measurement points → regular grid → IDW interpolation →
> population-weighted exposure → equity / inequality summary

All spatial data uses **EPSG:32632** (UTM zone 32N), with Milan air-quality
(NO₂) data as the worked example.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

Dependencies: geopandas, shapely ≥ 2.0, numpy, pandas, pyproj. Python ≥ 3.10.

## Usage

```python
from geoexposure import (
    load_sample_data, create_regular_grid, idw_interpolation,
    population_weighted_exposure, area_weighted_mean, exposure_bias,
    exposure_inequality_summary,
)

data = load_sample_data()                         # boundary, stations, population_grid
grid = create_regular_grid(data["boundary"], cell_size=500)
grid = idw_interpolation(data["stations"], grid, value_col="no2")
# ... join population onto the grid ...
pwe  = population_weighted_exposure(grid, "idw_value", "population")
mean = area_weighted_mean(grid, "idw_value")
bias = exposure_bias(pwe, mean)
```

See [`examples/basic_workflow.py`](examples/basic_workflow.py) for the full chain.

## API

| Module | Function | Purpose |
|---|---|---|
| `grid` | `create_regular_grid` | square grid over a boundary |
| `interpolation` | `idw_interpolation` | IDW from points to grid (`idw_value`) |
| `exposure` | `population_weighted_exposure` | PWE scalar |
| `exposure` | `area_weighted_mean` | plain area mean |
| `exposure` | `exposure_bias` | % bias PWE vs. mean |
| `equity` | `exposure_inequality_summary` | high/low exposure groups |
| `io` | `load_sample_data` | bundled Milan datasets |

**Terminology:** a grid cell carries a *concentration* (`idw_value`); only the
population-aggregated scalar is called an *exposure*.

## Testing

```bash
pip install -e ".[test]"
pytest
```

## Contributing

Contributions are welcome. Please keep the five-module layout
(`grid` / `interpolation` / `exposure` / `equity` / `io`), the fixed function
signatures, and EPSG:32632 throughout. Add a unit test for any new behaviour.

## License

MIT — see [LICENSE](LICENSE).

# -*- coding: utf-8 -*-
"""Optional plotting helpers for geoexposure outputs.

These require ``matplotlib``. The core analysis modules do not import it, so the
library still works without matplotlib installed; only this module needs it.
"""


def _require_matplotlib():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise ImportError(
            "Plotting requires matplotlib. Install it with: pip install matplotlib"
        ) from exc
    return plt


def plot_choropleth(gdf, column, title=None, cmap="viridis", points_gdf=None,
                    figsize=(8, 8), ax=None, savepath=None):
    """Draw a choropleth map of ``column`` over a polygon GeoDataFrame.

    Parameters
    ----------
    gdf : GeoDataFrame      polygons carrying ``column``
    column : str            column to colour by (e.g. 'idw_value')
    title : str, optional   plot title
    cmap : str              matplotlib colormap name
    points_gdf : GeoDataFrame, optional
        points to overlay (e.g. monitoring stations)
    figsize : tuple         figure size when creating a new axis
    ax : matplotlib Axes, optional
        draw on an existing axis instead of creating one
    savepath : str or Path, optional
        if given, save the figure as a PNG (150 dpi)

    Returns
    -------
    matplotlib Axes
    """
    plt = _require_matplotlib()
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)

    gdf.plot(column=column, cmap=cmap, legend=True, ax=ax,
             legend_kwds={"shrink": 0.6, "label": column}, edgecolor="none")
    if points_gdf is not None:
        points_gdf.plot(ax=ax, color="red", markersize=20, marker="^",
                        edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_title(title or column)
    ax.set_axis_off()
    ax.set_aspect("equal")

    if savepath is not None:
        ax.figure.savefig(savepath, dpi=150, bbox_inches="tight")
    return ax

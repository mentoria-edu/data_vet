from enum import StrEnum
from pathlib import Path
from typing import Literal

import geopandas as gpd


class _AllowedOutputCRS(StrEnum):
    LATLON = "EPSG:4326"
    METERS = "EPSG:3857"


CRS_LATLON = _AllowedOutputCRS.LATLON.value
CRS_METERS = _AllowedOutputCRS.METERS.value


class ShapefileHandler:
    """Handle operations for a Shapefile source.

    This class loads a Shapefile from disk and provides methods to:
        - Return its content as a GeoDataFrame.
        - Export its content as a GeoJSON string or file.

    The Shapefile is lazily loaded and cached after the first read.
    """

    def __init__(self, shapefile_path: str | Path):
        """Initialize the ShapefileHandler.

        Args:
            shapefile_path (str | Path): Path to the input Shapefile
                (.shp). The file must exist.

        Raises:
            FileNotFoundError: If the provided Shapefile path does not exist.
        """
        self._shapefile_path = Path(shapefile_path)

        if not self._shapefile_path.is_file():
            raise FileNotFoundError(
                f"Shapefile not found: {self._shapefile_path}"
            )

        self._gdf = None

    def _load(self):
        """Load the Shapefile into a GeoDataFrame.

        The file is read only once and cached for subsequent calls.

        Returns:
            gpd.GeoDataFrame: The loaded GeoDataFrame.
        """
        if self._gdf is None:
            self._gdf = gpd.read_file(self._shapefile_path)
        return self._gdf

    @staticmethod
    def _validate_output_crs(output_crs: str | None):
        if output_crs is None:
            return

        try:
            _AllowedOutputCRS(output_crs)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in _AllowedOutputCRS)
            raise ValueError(
                f"Invalid output_crs: {output_crs}. Allowed values: {allowed}."
            ) from exc

    def to_geodataframe(
        self, output_crs: Literal["EPSG:4326", "EPSG:3857"] | None = None
    ):
        """Return the Shapefile content as a GeoDataFrame.

        Args:
            output_crs (Literal["EPSG:4326", "EPSG:3857"] | None, optional):
                Target CRS. Supported
                values are "EPSG:4326" (latlon) and "EPSG:3857" (meters). If
                provided and the source has a defined CRS, the GeoDataFrame is
                reprojected before being returned. Defaults to None.

        Returns:
            gpd.GeoDataFrame: A copy of the GeoDataFrame, optionally
                reprojected.
        """
        gdf = self._load()
        self._validate_output_crs(output_crs)

        if output_crs is not None and gdf.crs is not None:
            return gdf.to_crs(output_crs)

        return gdf.copy()

    def to_geojson(
        self,
        output_path: str | Path | None = None,
        output_crs: Literal["EPSG:4326", "EPSG:3857"] = CRS_LATLON,
    ):
        """Export the Shapefile content as a GeoJSON string or file.

        Args:
            output_path (str | Path | None, optional): If provided,
                the GeoJSON content is written to this path. If None,
                only the GeoJSON string is returned. Defaults to None.
            output_crs (Literal["EPSG:4326", "EPSG:3857"], optional):
                Target CRS for the GeoJSON
                export. Supported values are "EPSG:4326" (latlon) and
                "EPSG:3857" (meters). The data is reprojected before
                serialization if a CRS is defined. Defaults to "EPSG:4326".

        Returns:
            str: The GeoJSON representation of the data.
        """
        gdf = self._load()
        self._validate_output_crs(output_crs)

        if output_crs is not None and gdf.crs is not None:
            gdf = gdf.to_crs(output_crs)

        geojson_str = gdf.to_json()

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(geojson_str, encoding="utf-8")

        return geojson_str

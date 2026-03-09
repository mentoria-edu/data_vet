import json
from pathlib import Path

import geopandas as gpd
from pyproj import CRS

from .crs import _AllowedOutputCRS
from .validators import (
    _ensure_output_type_allowed_crs,
    _ensure_output_type_path,
)


class ShapefileHandler:
    """Handle operations for a Shapefile source.

    This class loads a Shapefile from disk and provides methods to:
        - Return its content as a GeoDataFrame.
        - Return its content as a GeoJSON string.
        - Export data to GeoJSON or CSV files.

    The Shapefile is lazily loaded and cached after the first read.
    """

    def __init__(self, shapefile_path: Path):
        """Initialize the ShapefileHandler.

        Args:
            shapefile_path (Path): Path to the input Shapefile
                (.shp). The file must exist.

        Raises:
            FileNotFoundError: If the provided Shapefile path does not exist.
        """
        self._shapefile_path = shapefile_path

        if not self._shapefile_path.is_file():
            raise FileNotFoundError(
                f"Shapefile not found: {self._shapefile_path}"
            )

        self._gdf = None

    def _load(self) -> gpd.GeoDataFrame:
        """Load the Shapefile into a GeoDataFrame.

        The file is read only once and cached for subsequent calls.

        Returns:
            gpd.GeoDataFrame: The loaded GeoDataFrame.
        """
        if self._gdf is None:
            self._gdf = gpd.read_file(self._shapefile_path)
        return self._gdf

    def to_geodataframe(
        self,
        output_crs: _AllowedOutputCRS,
    ) -> gpd.GeoDataFrame:
        """Return the Shapefile content as a GeoDataFrame.

        Args:
            output_crs (_AllowedOutputCRS):
                Target CRS defined by business rules.
                Use `_AllowedOutputCRS.LATLON` or `_AllowedOutputCRS.METERS`.

        Returns:
            gpd.GeoDataFrame: A copy with a defined CRS.
                If source CRS is missing, `output_crs` is assigned.
                If source CRS differs, data is reprojected.
        """
        output_crs = _ensure_output_type_allowed_crs(output_crs)
        gdf = self._load()

        if gdf.crs is None:
            gdf_with_crs = gdf.copy()
            return gdf_with_crs.set_crs(output_crs.crs)

        current_crs = CRS.from_user_input(gdf.crs)
        if current_crs.equals(output_crs.crs):
            return gdf.copy()

        return gdf.to_crs(output_crs.crs)

    def to_geojson(
        self,
        output_crs: _AllowedOutputCRS,
    ) -> str:
        """Return the Shapefile content as a GeoJSON string.

        Args:
            output_crs (_AllowedOutputCRS):
                Target CRS for GeoJSON serialization.

        Returns:
            str: GeoJSON serialized with `json` for stable JSON output.
        """
        output_crs = _ensure_output_type_allowed_crs(output_crs)
        gdf = self.to_geodataframe(output_crs=output_crs)
        geojson_obj = json.loads(gdf.to_json())
        return json.dumps(geojson_obj, ensure_ascii=False)

    def export_geojson(
        self,
        output_path: Path,
        output_crs: _AllowedOutputCRS,
    ) -> Path:
        """Export Shapefile content to a GeoJSON file.

        Args:
            output_path (Path): Destination path for the GeoJSON file.
            output_crs (_AllowedOutputCRS):
                Target CRS for exported data.

        Returns:
            Path: The output file path.
        """
        output_path = _ensure_output_type_path(output_path)
        output_crs = _ensure_output_type_allowed_crs(output_crs)

        geojson_str = self.to_geojson(output_crs=output_crs)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(geojson_str, encoding="utf-8")

        return output_path

    def export_csv(
        self,
        output_path: Path,
        output_crs: _AllowedOutputCRS,
    ) -> Path:
        """Export Shapefile content to a CSV file.

        Args:
            output_path (Path): Destination path for the output CSV file.
            output_crs (_AllowedOutputCRS):
                Target CRS for exported data.

        Returns:
            Path: The output CSV file path.
        """
        output_path = _ensure_output_type_path(output_path)
        output_crs = _ensure_output_type_allowed_crs(output_crs)

        gdf = self.to_geodataframe(output_crs=output_crs)
        csv_df = gdf.copy()
        csv_df["geometry"] = csv_df.geometry.to_wkt()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        csv_df.to_csv(output_path, index=False, encoding="utf-8")

        return output_path

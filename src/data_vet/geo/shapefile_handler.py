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

    The Shapefile is eagerly loaded and normalized to the target CRS
    during initialization.
    """

    def __init__(
        self,
        shapefile_path: Path,
        output_crs: _AllowedOutputCRS,
    ):
        """Initialize the ShapefileHandler.

        Args:
            shapefile_path (Path): Path to the input Shapefile
                (.shp). The file must exist.
            output_crs (_AllowedOutputCRS): Target CRS used to keep
                in-memory data normalized.

        Raises:
            FileNotFoundError: If the provided Shapefile path does not exist.
            ValueError: If source data does not define a CRS.
        """
        self._shapefile_path = shapefile_path
        self._output_crs = _ensure_output_type_allowed_crs(output_crs)

        if not self._shapefile_path.is_file():
            raise FileNotFoundError(
                f"Shapefile not found: {self._shapefile_path}"
            )

        source_geodataframe = gpd.read_file(self._shapefile_path)

        if source_geodataframe.crs is None:
            raise ValueError(
                "Source Shapefile must define a CRS before processing."
            )

        source_crs = CRS.from_user_input(source_geodataframe.crs)
        if source_crs.equals(self._output_crs.crs):
            self._gdf = source_geodataframe
            return

        self._gdf = source_geodataframe.to_crs(self._output_crs.crs)

    def change_crs(self, output_crs: _AllowedOutputCRS) -> None:
        """Reproject the in-memory GeoDataFrame to another CRS.

        Args:
            output_crs (_AllowedOutputCRS): Target CRS defined by
                business rules.
        """
        self._output_crs = _ensure_output_type_allowed_crs(output_crs)
        current_crs = CRS.from_user_input(self._gdf.crs)

        if current_crs.equals(self._output_crs.crs):
            return

        self._gdf = self._gdf.to_crs(self._output_crs.crs)

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        """Return the Shapefile content as a GeoDataFrame.

        Returns:
            gpd.GeoDataFrame: A copy of the in-memory GeoDataFrame.
        """
        return self._gdf.copy()

    def to_geojson(self) -> str:
        """Return the Shapefile content as a GeoJSON string.

        Returns:
            str: GeoJSON serialized with `json` for stable JSON output.
        """
        gdf = self.to_geodataframe()
        geojson_obj = json.loads(gdf.to_json())
        return json.dumps(geojson_obj, ensure_ascii=False)

    def export_geojson(
        self,
        output_path: Path,
    ) -> Path:
        """Export Shapefile content to a GeoJSON file.

        Args:
            output_path (Path): Destination path for the GeoJSON file.

        Returns:
            Path: The output file path.
        """
        output_path = _ensure_output_type_path(output_path)

        geojson_str = self.to_geojson()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(geojson_str, encoding="utf-8")

        return output_path

    def export_csv(
        self,
        output_path: Path,
    ) -> Path:
        """Export Shapefile content to a CSV file.

        Args:
            output_path (Path): Destination path for the output CSV file.

        Returns:
            Path: The output CSV file path.
        """
        output_path = _ensure_output_type_path(output_path)

        gdf = self.to_geodataframe()
        csv_df = gdf.copy()
        csv_df["geometry"] = csv_df.geometry.to_wkt()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        csv_df.to_csv(output_path, index=False, encoding="utf-8")

        return output_path

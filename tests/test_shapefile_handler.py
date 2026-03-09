"""Tests for `ShapefileHandler`."""

import json
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Point

from data_vet.geo.crs import _AllowedOutputCRS
from data_vet.geo.shapefile_handler import ShapefileHandler


@pytest.fixture
def simple_shapefile_path(tmp_path: Path) -> Path:
    """Create a simple Shapefile fixture.

    Args:
        tmp_path: Temporary directory path provided by pytest.

    Returns:
        Path to the created Shapefile.
    """
    shapefile_path = tmp_path / "simple_feature.shp"
    geodataframe = gpd.GeoDataFrame(
        {"id": [1], "name": ["feature_1"]},
        geometry=[Point(-46.6333, -23.5505)],
        crs=_AllowedOutputCRS.LATLON.crs,
    )
    geodataframe.to_file(shapefile_path)
    return shapefile_path


@pytest.fixture
def shapefile_handler(simple_shapefile_path: Path) -> ShapefileHandler:
    """Create a `ShapefileHandler` fixture.

    Args:
        simple_shapefile_path: Valid path to a temporary Shapefile.

    Returns:
        Instantiated `ShapefileHandler`.
    """
    return ShapefileHandler(simple_shapefile_path)


def test_init_raises_file_not_found_error_for_invalid_path(
    tmp_path: Path,
) -> None:
    """Ensure `__init__` raises `FileNotFoundError` for invalid paths.

    Args:
        tmp_path: Temporary directory path provided by pytest.
    """
    invalid_path = tmp_path / "missing.shp"
    with pytest.raises(FileNotFoundError):
        ShapefileHandler(invalid_path)


def test_to_geodataframe_returns_geodataframe(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geodataframe` returns a `GeoDataFrame`.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    result = shapefile_handler.to_geodataframe(
        output_crs=_AllowedOutputCRS.LATLON
    )
    assert isinstance(result, gpd.GeoDataFrame)


def test_to_geodataframe_sets_requested_crs_when_different(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geodataframe` reprojects when CRS differs.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    output_crs = _AllowedOutputCRS.METERS
    result = shapefile_handler.to_geodataframe(output_crs=output_crs)
    assert result.crs.equals(output_crs.crs)


def test_to_geodataframe_keeps_requested_crs_when_equal(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geodataframe` returns requested CRS when already equal.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    output_crs = _AllowedOutputCRS.LATLON
    result = shapefile_handler.to_geodataframe(output_crs=output_crs)
    assert result.crs.equals(output_crs.crs)


def test_to_geojson_returns_string(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geojson` returns a string.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    result = shapefile_handler.to_geojson(output_crs=_AllowedOutputCRS.LATLON)
    assert isinstance(result, str)


def test_to_geojson_matches_geodataframe_json_when_crs_is_different(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geojson` reflects requested CRS when it differs.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    output_crs = _AllowedOutputCRS.METERS
    expected_geojson = shapefile_handler.to_geodataframe(
        output_crs=output_crs
    ).to_json()
    result_geojson = shapefile_handler.to_geojson(output_crs=output_crs)
    assert json.loads(result_geojson) == json.loads(expected_geojson)


def test_to_geojson_matches_geodataframe_json_when_crs_is_equal(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geojson` reflects requested CRS when it is equal.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    output_crs = _AllowedOutputCRS.LATLON
    expected_geojson = shapefile_handler.to_geodataframe(
        output_crs=output_crs
    ).to_json()
    result_geojson = shapefile_handler.to_geojson(output_crs=output_crs)
    assert json.loads(result_geojson) == json.loads(expected_geojson)


def test_export_geojson_returns_path(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure `export_geojson` returns a `Path`.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_path = tmp_path / "output.geojson"
    result = shapefile_handler.export_geojson(
        output_path=output_path,
        output_crs=_AllowedOutputCRS.LATLON,
    )
    assert isinstance(result, Path)


def test_export_geojson_creates_output_file(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure `export_geojson` creates the output file.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_path = tmp_path / "output.geojson"
    shapefile_handler.export_geojson(
        output_path=output_path,
        output_crs=_AllowedOutputCRS.LATLON,
    )
    assert output_path.is_file()


def test_export_geojson_matches_in_memory_geojson(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure exported GeoJSON equals in-memory `to_geojson` output.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_crs = _AllowedOutputCRS.METERS
    output_path = tmp_path / "memory_match.geojson"

    in_memory_geojson = shapefile_handler.to_geojson(output_crs=output_crs)

    shapefile_handler.export_geojson(
        output_path=output_path,
        output_crs=output_crs,
    )

    exported_geojson = output_path.read_text(encoding="utf-8")

    assert exported_geojson == in_memory_geojson


def test_export_geojson_matches_in_memory_geojson_when_crs_is_equal(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure exported GeoJSON equals memory output when CRS is equal.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_crs = _AllowedOutputCRS.LATLON
    output_path = tmp_path / "memory_match_equal.geojson"

    in_memory_geojson = shapefile_handler.to_geojson(output_crs=output_crs)

    shapefile_handler.export_geojson(
        output_path=output_path,
        output_crs=output_crs,
    )

    exported_geojson = output_path.read_text(encoding="utf-8")

    assert exported_geojson == in_memory_geojson


def test_export_csv_returns_path(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure `export_csv` returns a `Path`.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_path = tmp_path / "output.csv"
    result = shapefile_handler.export_csv(
        output_path=output_path,
        output_crs=_AllowedOutputCRS.LATLON,
    )
    assert isinstance(result, Path)


def test_export_csv_creates_output_file(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure `export_csv` creates the output file.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_path = tmp_path / "output.csv"
    shapefile_handler.export_csv(
        output_path=output_path,
        output_crs=_AllowedOutputCRS.LATLON,
    )
    assert output_path.is_file()


def test_export_csv_matches_in_memory_csv_when_crs_is_different(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure exported CSV equals memory-equivalent CSV for different CRS.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_crs = _AllowedOutputCRS.METERS
    output_path = tmp_path / "memory_match.csv"

    in_memory_geodataframe = shapefile_handler.to_geodataframe(
        output_crs=output_crs
    )
    expected_dataframe = in_memory_geodataframe.copy()
    expected_dataframe["geometry"] = expected_dataframe.geometry.to_wkt()
    expected_csv = expected_dataframe.to_csv(index=False, encoding="utf-8")

    shapefile_handler.export_csv(
        output_path=output_path,
        output_crs=output_crs,
    )

    exported_csv = output_path.read_text(encoding="utf-8")

    assert exported_csv == expected_csv


def test_export_csv_matches_in_memory_csv_when_crs_is_equal(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure exported CSV equals memory-equivalent CSV for equal CRS.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_crs = _AllowedOutputCRS.LATLON
    output_path = tmp_path / "memory_match_equal.csv"

    in_memory_geodataframe = shapefile_handler.to_geodataframe(
        output_crs=output_crs
    )
    expected_dataframe = in_memory_geodataframe.copy()
    expected_dataframe["geometry"] = expected_dataframe.geometry.to_wkt()
    expected_csv = expected_dataframe.to_csv(index=False, encoding="utf-8")

    shapefile_handler.export_csv(
        output_path=output_path,
        output_crs=output_crs,
    )

    exported_csv = output_path.read_text(encoding="utf-8")

    assert exported_csv == expected_csv

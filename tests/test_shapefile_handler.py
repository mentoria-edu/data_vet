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
def shapefile_without_crs_path(tmp_path: Path) -> Path:
    """Create a Shapefile fixture without CRS metadata.

    Args:
        tmp_path: Temporary directory path provided by pytest.

    Returns:
        Path to the created Shapefile without CRS.
    """
    shapefile_path = tmp_path / "feature_without_crs.shp"
    geodataframe = gpd.GeoDataFrame(
        {"id": [1], "name": ["feature_without_crs"]},
        geometry=[Point(-46.6333, -23.5505)],
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
    return ShapefileHandler(
        shapefile_path=simple_shapefile_path,
        output_crs=_AllowedOutputCRS.LATLON,
    )


def test_init_raises_file_not_found_error_for_invalid_path(
    tmp_path: Path,
) -> None:
    """Ensure `__init__` raises `FileNotFoundError` for invalid path.

    Args:
        tmp_path: Temporary directory path provided by pytest.
    """
    invalid_path = tmp_path / "missing.shp"

    with pytest.raises(FileNotFoundError):
        ShapefileHandler(
            shapefile_path=invalid_path,
            output_crs=_AllowedOutputCRS.LATLON,
        )


def test_init_raises_type_error_for_invalid_output_crs(
    simple_shapefile_path: Path,
) -> None:
    """Ensure `__init__` validates `output_crs` type.

    Args:
        simple_shapefile_path: Valid path to a temporary Shapefile.
    """
    with pytest.raises(TypeError):
        ShapefileHandler(
            shapefile_path=simple_shapefile_path,
            output_crs="EPSG:4326",  # type: ignore[arg-type]
        )


def test_init_raises_value_error_when_source_crs_is_missing(
    shapefile_without_crs_path: Path,
) -> None:
    """Ensure `__init__` raises `ValueError` when source CRS is missing.

    Args:
        shapefile_without_crs_path: Path to a Shapefile without CRS.
    """
    with pytest.raises(ValueError):
        ShapefileHandler(
            shapefile_path=shapefile_without_crs_path,
            output_crs=_AllowedOutputCRS.LATLON,
        )


def test_init_keeps_crs_when_equal(simple_shapefile_path: Path) -> None:
    """Ensure `__init__` keeps source CRS when already equal.

    Args:
        simple_shapefile_path: Valid path to a temporary Shapefile.
    """
    shapefile_handler = ShapefileHandler(
        shapefile_path=simple_shapefile_path,
        output_crs=_AllowedOutputCRS.LATLON,
    )
    result = shapefile_handler.to_geodataframe()
    assert result.crs.equals(_AllowedOutputCRS.LATLON.crs)


def test_init_reprojects_crs_when_different(
    simple_shapefile_path: Path,
) -> None:
    """Ensure `__init__` reprojects source CRS when it differs.

    Args:
        simple_shapefile_path: Valid path to a temporary Shapefile.
    """
    shapefile_handler = ShapefileHandler(
        shapefile_path=simple_shapefile_path,
        output_crs=_AllowedOutputCRS.METERS,
    )
    result = shapefile_handler.to_geodataframe()
    assert result.crs.equals(_AllowedOutputCRS.METERS.crs)


def test_to_geodataframe_returns_geodataframe(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geodataframe` returns a `GeoDataFrame`.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    result = shapefile_handler.to_geodataframe()
    assert isinstance(result, gpd.GeoDataFrame)


def test_to_geodataframe_returns_copy(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geodataframe` returns a defensive copy.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    geodataframe_copy = shapefile_handler.to_geodataframe()
    geodataframe_copy.loc[:, "name"] = "changed_value"

    untouched_geodataframe = shapefile_handler.to_geodataframe()
    assert untouched_geodataframe.loc[0, "name"] == "feature_1"


def test_change_crs_reprojects_in_memory_data(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `change_crs` reprojects in-memory data.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    shapefile_handler.change_crs(output_crs=_AllowedOutputCRS.METERS)
    result = shapefile_handler.to_geodataframe()
    assert result.crs.equals(_AllowedOutputCRS.METERS.crs)


def test_change_crs_raises_type_error_for_invalid_output_crs(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `change_crs` validates `output_crs` type.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    with pytest.raises(TypeError):
        shapefile_handler.change_crs(output_crs="EPSG:3857")  # type: ignore[arg-type]


def test_to_geojson_returns_string(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geojson` returns a string.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    result = shapefile_handler.to_geojson()
    assert isinstance(result, str)


def test_to_geojson_matches_geodataframe_json(
    shapefile_handler: ShapefileHandler,
) -> None:
    """Ensure `to_geojson` matches `to_geodataframe().to_json()`.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
    """
    expected_geojson = shapefile_handler.to_geodataframe().to_json()
    result_geojson = shapefile_handler.to_geojson()
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
    result = shapefile_handler.export_geojson(output_path=output_path)
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
    shapefile_handler.export_geojson(output_path=output_path)
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
    output_path = tmp_path / "memory_match.geojson"
    in_memory_geojson = shapefile_handler.to_geojson()

    shapefile_handler.export_geojson(output_path=output_path)
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
    result = shapefile_handler.export_csv(output_path=output_path)
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
    shapefile_handler.export_csv(output_path=output_path)
    assert output_path.is_file()


def test_export_csv_matches_in_memory_csv(
    shapefile_handler: ShapefileHandler,
    tmp_path: Path,
) -> None:
    """Ensure exported CSV equals memory-equivalent CSV.

    Args:
        shapefile_handler: Fixture instance of `ShapefileHandler`.
        tmp_path: Temporary directory path provided by pytest.
    """
    output_path = tmp_path / "memory_match.csv"

    in_memory_geodataframe = shapefile_handler.to_geodataframe()
    expected_dataframe = in_memory_geodataframe.copy()
    expected_dataframe["geometry"] = expected_dataframe.geometry.to_wkt()
    expected_csv = expected_dataframe.to_csv(index=False, encoding="utf-8")

    shapefile_handler.export_csv(output_path=output_path)
    exported_csv = output_path.read_text(encoding="utf-8")

    assert exported_csv == expected_csv

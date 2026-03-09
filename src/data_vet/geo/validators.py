"""Validation helpers for geo output arguments."""

from pathlib import Path

from .crs import _AllowedOutputCRS


def _ensure_output_type_allowed_crs(
    output_crs: _AllowedOutputCRS,
) -> _AllowedOutputCRS:
    """Ensure `output_crs` is an allowed `_AllowedOutputCRS` value."""
    if not isinstance(output_crs, _AllowedOutputCRS):
        raise TypeError(
            "output_crs must be an instance of _AllowedOutputCRS."
        )
    return output_crs


def _ensure_output_type_path(output_path: Path) -> Path:
    """Ensure `output_path` is a `pathlib.Path` instance."""
    if not isinstance(output_path, Path):
        raise TypeError("output_path must be an instance of pathlib.Path.")
    return output_path

"""CRS definitions constrained by business rules."""

from enum import StrEnum

from pyproj import CRS


class _AllowedOutputCRS(StrEnum):
    """Allowed output CRS values enforced by business rules."""

    LATLON = "EPSG:4326"
    METERS = "EPSG:3857"

    @property
    def crs(self) -> CRS:
        """Return the enum value as a `pyproj.CRS` instance."""
        return CRS.from_user_input(self.value)

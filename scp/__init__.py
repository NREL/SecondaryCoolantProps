import importlib.metadata

from scp.api import available_fluids, available_properties, get_fluid
from scp.user_defined import UserDefinedFluid, UserDefinedProperties

try:
    VERSION = importlib.metadata.version("SecondaryCoolantProps")
except importlib.metadata.PackageNotFoundError:
    VERSION = "0+unknown"

__all__ = [
    "VERSION",
    "UserDefinedFluid",
    "UserDefinedProperties",
    "available_fluids",
    "available_properties",
    "get_fluid",
]

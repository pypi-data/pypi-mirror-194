"""Part class."""
# Standard Modules
from dataclasses import dataclass

# Local Modules
from cofactr.schema.flagship_v3.part import Part as FlagshipV3Part


@dataclass
class Part(FlagshipV3Part):
    """Part."""

    lifecycle_status: str

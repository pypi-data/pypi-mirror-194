"""Definition of types of kinetic parameters."""
from enum import Enum


class KineticParameterType(Enum):
    """Type of kinetic parameters supported in ENKIE."""
    K_M = 1
    K_CAT_FORWARD = 2
    K_CAT_BACKWARD = 3
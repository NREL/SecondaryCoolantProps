from collections.abc import Callable
from dataclasses import dataclass
from numbers import Real
from typing import TypeAlias

from scp.base_fluid import BaseFluid

TemperatureProperty: TypeAlias = float | Callable[[float], float]
FreezingPointProperty: TypeAlias = float | Callable[[float | None], float]


@dataclass(frozen=True)
class UserDefinedProperties:
    """
    Core user-defined fluid properties.
    """

    viscosity: TemperatureProperty
    specific_heat: TemperatureProperty
    density: TemperatureProperty
    conductivity: TemperatureProperty
    freeze_point: FreezingPointProperty = 0.0

    def __post_init__(self) -> None:
        for prop_name in ("viscosity", "specific_heat", "density", "conductivity"):
            _validate_property_value(prop_name, getattr(self, prop_name))
        _validate_property_value("freeze_point", self.freeze_point)


def _validate_property_value(prop_name: str, prop_value: object) -> None:
    """
    Validate that a user-defined property can be evaluated later.

    @param prop_name: Property name for error messages
    @param prop_value: User-defined property value
    """
    if callable(prop_value):
        return
    if isinstance(prop_value, Real) and not isinstance(prop_value, bool):
        return

    msg = f'User-defined property "{prop_name}" must be a real number or callable'
    raise TypeError(msg)


class UserDefinedFluid(BaseFluid):
    """
    A fluid whose core properties are provided by the user.

    Each temperature-dependent property may be supplied as either a constant
    value or a callable that accepts temperature in Celsius and returns the
    property value in the same units used by :class:`scp.base_fluid.BaseFluid`.
    """

    def __init__(
        self,
        properties: UserDefinedProperties,
        *,
        name: str = "UserDefinedFluid",
        t_min: float = -273.15,
        t_max: float = 1000.0,
    ) -> None:
        """
        Construct a user-defined fluid.

        @param properties: User-defined fluid property values
        @param name: Descriptive fluid name
        @param t_min: Minimum valid temperature in Celsius
        @param t_max: Maximum valid temperature in Celsius
        """

        self._fluid_name = name
        self._properties = properties
        super().__init__(t_min, t_max)

    @property
    def fluid_name(self) -> str:
        """
        Returns the descriptive fluid name.

        @return: Fluid name
        """
        return self._fluid_name

    def _evaluate_temperature_property(self, prop: TemperatureProperty, temp: float) -> float:
        """
        Evaluate a constant or callable temperature-dependent property.

        @param prop: Property value or function
        @param temp: Fluid temperature in Celsius
        @return: Evaluated property value
        """
        temp = self._check_temperature(temp)
        if callable(prop):
            return float(prop(temp))
        return float(prop)

    def viscosity(self, temp: float) -> float:
        """
        Returns the user-defined dynamic viscosity.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Dynamic viscosity in [Pa-s]
        """
        return self._evaluate_temperature_property(self._properties.viscosity, temp)

    def specific_heat(self, temp: float) -> float:
        """
        Returns the user-defined specific heat.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Specific heat in [J/kg-K]
        """
        return self._evaluate_temperature_property(self._properties.specific_heat, temp)

    def density(self, temp: float) -> float:
        """
        Returns the user-defined density.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Density in [kg/m3]
        """
        return self._evaluate_temperature_property(self._properties.density, temp)

    def conductivity(self, temp: float) -> float:
        """
        Returns the user-defined thermal conductivity.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Thermal conductivity in [W/m-K]
        """
        return self._evaluate_temperature_property(self._properties.conductivity, temp)

    def freeze_point(self, x: float | None = None) -> float:
        """
        Returns the user-defined freezing point.

        @param x: Optional concentration fraction
        @return: Freezing point temperature in Celsius
        """
        if callable(self._properties.freeze_point):
            return float(self._properties.freeze_point(x))
        return float(self._properties.freeze_point)

from collections.abc import Callable, Mapping
from math import isfinite
from typing import cast

from scp._numeric import is_float
from scp.base_fluid import BaseFluid
from scp.ethyl_alcohol import EthylAlcohol
from scp.ethylene_glycol import EthyleneGlycol
from scp.methyl_alcohol import MethylAlcohol
from scp.propylene_glycol import PropyleneGlycol
from scp.user_defined import FreezingPointProperty, TemperatureProperty, UserDefinedFluid, UserDefinedProperties
from scp.water import Water

FluidFactory = Callable[[float], BaseFluid]

_FLUID_FACTORIES: dict[str, FluidFactory] = {
    "ethyl_alcohol": EthylAlcohol,
    "ethylene_glycol": EthyleneGlycol,
    "methyl_alcohol": MethylAlcohol,
    "propylene_glycol": PropyleneGlycol,
}
_USER_DEFINED_REQUIRED_PROPERTY_KEYS = (
    "viscosity",
    "specific_heat",
    "density",
    "conductivity",
)
_PROPERTY_NAMES = (
    *_USER_DEFINED_REQUIRED_PROPERTY_KEYS,
    "prandtl",
    "thermal_diffusivity",
    "freeze_point",
)
_USER_DEFINED_PROPERTY_KEYS = (
    *_USER_DEFINED_REQUIRED_PROPERTY_KEYS,
    "freeze_point",
)


def _normalize_key(value: str) -> str:
    """
    Normalize a user-facing fluid or property key.

    @param value: User-facing key
    @return: Normalized key
    """
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def available_fluids(*, include_user_defined: bool = True) -> tuple[str, ...]:
    """
    Return the fluid keys accepted by :func:`get_fluid`.

    @param include_user_defined: Include the key for user-defined fluids
    @return: Supported fluid keys
    """
    fluids = ("water", *_FLUID_FACTORIES.keys())
    if include_user_defined:
        return (*fluids, "user_defined")
    return fluids


def available_properties() -> tuple[str, ...]:
    """
    Return the property keys supported by fluid instances and the CLI.

    @return: Supported property keys
    """
    return _PROPERTY_NAMES


def _float_option(option_name: str, option_value: object) -> float:
    """
    Convert a user-defined fluid option to a float.

    @param option_name: Option name for error messages
    @param option_value: User-defined option value
    @return: Float value
    """
    if is_float(option_value):
        float_value = float(option_value)
        if isfinite(float_value):
            return float_value

        msg = f'User-defined option "{option_name}" must be finite'
        raise ValueError(msg)

    msg = f'User-defined option "{option_name}" must be an int or float'
    raise TypeError(msg)


def _collect_user_defined_options(
    properties: UserDefinedProperties | Mapping[str, object] | None,
    options: dict[str, object],
) -> tuple[UserDefinedProperties, str, float, float]:
    """
    Collect user-defined fluid options into a validated property object.

    @param properties: User-defined properties object or mapping
    @param options: Additional user-defined fluid options
    @return: Properties, name, minimum temperature, and maximum temperature
    """
    name = str(options.pop("name", "UserDefinedFluid"))
    t_min = _float_option("t_min", options.pop("t_min", -273.15))
    t_max = _float_option("t_max", options.pop("t_max", 1000.0))

    if isinstance(properties, UserDefinedProperties):
        if options:
            msg = f"Unexpected user-defined fluid options: {', '.join(sorted(options))}"
            raise ValueError(msg)
        return properties, name, t_min, t_max

    property_values = dict(properties or {})
    property_values.update(options)

    unknown_properties = set(property_values).difference(_USER_DEFINED_PROPERTY_KEYS)
    if unknown_properties:
        msg = f"Unexpected user-defined fluid properties: {', '.join(sorted(unknown_properties))}"
        raise ValueError(msg)

    missing_properties = [
        prop_name for prop_name in _USER_DEFINED_REQUIRED_PROPERTY_KEYS if prop_name not in property_values
    ]
    if missing_properties:
        msg = f"User-defined fluid is missing required properties: {', '.join(missing_properties)}"
        raise ValueError(msg)

    return (
        UserDefinedProperties(
            viscosity=cast(TemperatureProperty, property_values["viscosity"]),
            specific_heat=cast(TemperatureProperty, property_values["specific_heat"]),
            density=cast(TemperatureProperty, property_values["density"]),
            conductivity=cast(TemperatureProperty, property_values["conductivity"]),
            freeze_point=cast(FreezingPointProperty, property_values.get("freeze_point", 0.0)),
        ),
        name,
        t_min,
        t_max,
    )


def get_fluid(
    fluid: str,
    *,
    concentration: float = 0.0,
    properties: UserDefinedProperties | Mapping[str, object] | None = None,
    **user_defined_options: object,
) -> BaseFluid:
    """
    Construct a fluid from the user-facing API.

    @param fluid: Fluid key
    @param concentration: Mixture concentration fraction for built-in mixture fluids
    @param properties: User-defined property values
    @param user_defined_options: User-defined fluid options and property values
    @return: Fluid instance
    """

    fluid_key = _normalize_key(fluid)
    if (properties is not None or user_defined_options) and fluid_key != "user_defined":
        msg = "User-defined options can only be used with the user_defined fluid"
        raise ValueError(msg)
    if fluid_key == "water":
        if concentration != 0.0:
            msg = "Water does not accept a nonzero concentration"
            raise ValueError(msg)
        return Water()
    if fluid_key == "user_defined":
        user_properties, name, t_min, t_max = _collect_user_defined_options(properties, user_defined_options)

        return UserDefinedFluid(
            user_properties,
            name=name,
            t_min=t_min,
            t_max=t_max,
        )
    if fluid_key in _FLUID_FACTORIES:
        return _FLUID_FACTORIES[fluid_key](concentration)

    msg = f'Unsupported fluid "{fluid}". Supported fluids: {", ".join(available_fluids())}'
    raise ValueError(msg)

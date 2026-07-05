import pytest

from scp import UserDefinedProperties, available_fluids, available_properties, get_fluid
from scp.propylene_glycol import PropyleneGlycol
from scp.user_defined import UserDefinedFluid
from scp.water import Water


def test_available_fluids_includes_user_defined_by_default() -> None:
    assert available_fluids() == (
        "water",
        "ethyl_alcohol",
        "ethylene_glycol",
        "methyl_alcohol",
        "propylene_glycol",
        "user_defined",
    )
    assert "user_defined" not in available_fluids(include_user_defined=False)


def test_available_properties() -> None:
    assert available_properties() == (
        "viscosity",
        "specific_heat",
        "density",
        "conductivity",
        "prandtl",
        "thermal_diffusivity",
        "freeze_point",
    )


def test_get_fluid_returns_built_in_fluid() -> None:
    assert isinstance(get_fluid("water"), Water)

    pg_zero = get_fluid("propylene_glycol", concentration=0)
    assert isinstance(pg_zero, PropyleneGlycol)
    assert pg_zero.x == pytest.approx(0.0)

    pg = get_fluid("propylene-glycol", concentration=0.4)
    assert isinstance(pg, PropyleneGlycol)
    assert pg.x == pytest.approx(0.4)


def test_get_fluid_returns_user_defined_fluid() -> None:
    fluid = get_fluid(
        "user defined",
        name="CustomFluid",
        viscosity=0.002,
        specific_heat=3200.0,
        density=1050.0,
        conductivity=0.42,
        freeze_point=-12.0,
    )

    assert isinstance(fluid, UserDefinedFluid)
    assert fluid.fluid_name == "CustomFluid"
    assert fluid.density(20.0) == pytest.approx(1050.0)

    properties = UserDefinedProperties(
        viscosity=0.003,
        specific_heat=3100.0,
        density=1040.0,
        conductivity=0.4,
    )
    property_object_fluid = get_fluid("user_defined", properties=properties)

    assert isinstance(property_object_fluid, UserDefinedFluid)
    assert property_object_fluid.viscosity(20.0) == pytest.approx(0.003)


def test_get_fluid_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="Water does not accept"):
        get_fluid("water", concentration=0.2)

    with pytest.raises(ValueError, match="Unsupported fluid"):
        get_fluid("unknown")

    with pytest.raises(ValueError, match="missing required properties"):
        get_fluid("user_defined", viscosity=0.001)

    with pytest.raises(TypeError, match="viscosity"):
        get_fluid("user_defined", viscosity=None, specific_heat=1.0, density=1.0, conductivity=1.0)

    with pytest.raises(TypeError, match="t_min"):
        get_fluid(
            "user_defined",
            viscosity=0.001,
            specific_heat=1.0,
            density=1.0,
            conductivity=1.0,
            t_min=None,
        )

    with pytest.raises(ValueError, match="User-defined options"):
        get_fluid("water", viscosity=0.001)

    with pytest.raises(ValueError, match="User-defined options"):
        get_fluid("water", properties={"viscosity": 0.001})

    with pytest.raises(ValueError, match="Unexpected user-defined fluid options"):
        get_fluid(
            "user_defined",
            properties=UserDefinedProperties(
                viscosity=0.001,
                specific_heat=3200.0,
                density=1050.0,
                conductivity=0.42,
            ),
            viscosity=0.002,
        )

    with pytest.raises(ValueError, match="Unexpected user-defined fluid properties"):
        get_fluid(
            "user_defined",
            properties={
                "viscosity": 0.001,
                "specific_heat": 3200.0,
                "density": 1050.0,
                "conductivity": 0.42,
                "enthalpy": 100.0,
            },
        )


def test_get_fluid_returns_instances_for_property_evaluation() -> None:
    water = get_fluid("water")
    pg = get_fluid("propylene glycol", concentration=0.4)
    fluid = UserDefinedFluid(
        UserDefinedProperties(
            viscosity=0.002,
            specific_heat=3200.0,
            density=lambda temp: 1000.0 - temp,
            conductivity=0.42,
        ),
    )

    assert water.density(25.0) == pytest.approx(Water().density(25.0))
    assert pg.freeze_point(0.4) == pytest.approx(PropyleneGlycol(0.4).freeze_point(0.4))
    assert fluid.density(30.0) == pytest.approx(970.0)


def test_get_fluid_accepts_user_defined_properties_for_derived_properties() -> None:
    fluid = get_fluid(
        "user_defined",
        viscosity=0.002,
        specific_heat=3200.0,
        density=1050.0,
        conductivity=0.42,
    )

    assert fluid.thermal_diffusivity(20.0) == pytest.approx(1.25e-7)

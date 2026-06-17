from typing import Any, cast

import pytest

from scp.user_defined import UserDefinedFluid, UserDefinedProperties


def make_user_defined_fluid(**kwargs) -> UserDefinedFluid:
    properties = UserDefinedProperties(
        viscosity=kwargs.pop("viscosity", 0.002),
        specific_heat=kwargs.pop("specific_heat", 3200.0),
        density=kwargs.pop("density", 1050.0),
        conductivity=kwargs.pop("conductivity", 0.42),
        freeze_point=kwargs.pop("freeze_point", -12.0),
    )
    return UserDefinedFluid(properties, **kwargs)


def test_user_defined_fluid_accepts_constant_properties() -> None:
    fluid = make_user_defined_fluid(
        name="TestFluid",
        t_min=-20.0,
        t_max=80.0,
    )

    assert fluid.fluid_name == "TestFluid"
    assert fluid.viscosity(20.0) == pytest.approx(0.002)
    assert fluid.specific_heat(20.0) == pytest.approx(3200.0)
    assert fluid.density(20.0) == pytest.approx(1050.0)
    assert fluid.conductivity(20.0) == pytest.approx(0.42)
    assert fluid.freeze_point() == pytest.approx(-12.0)
    assert fluid.mu(20.0) == pytest.approx(0.002)
    assert fluid.cp(20.0) == pytest.approx(3200.0)
    assert fluid.rho(20.0) == pytest.approx(1050.0)
    assert fluid.k(20.0) == pytest.approx(0.42)
    assert fluid.prandtl(20.0) == pytest.approx(15.238095238)
    assert fluid.pr(20.0) == pytest.approx(15.238095238)
    assert fluid.thermal_diffusivity(20.0) == pytest.approx(1.25e-7)
    assert fluid.alpha(20.0) == pytest.approx(1.25e-7)


def test_user_defined_fluid_accepts_callable_properties() -> None:
    fluid = UserDefinedFluid(
        UserDefinedProperties(
            viscosity=lambda temp: 0.003 - 1.0e-5 * temp,
            specific_heat=lambda temp: 3000.0 + 2.0 * temp,
            density=lambda temp: 1000.0 - 0.5 * temp,
            conductivity=lambda temp: 0.3 + 1.0e-3 * temp,
            freeze_point=lambda temp: -30.0 * (temp or 0.0),
        ),
    )

    assert fluid.viscosity(10.0) == pytest.approx(0.0029)
    assert fluid.specific_heat(10.0) == pytest.approx(3020.0)
    assert fluid.density(10.0) == pytest.approx(995.0)
    assert fluid.conductivity(10.0) == pytest.approx(0.31)
    assert fluid.freeze_point(0.4) == pytest.approx(-12.0)


def test_user_defined_properties_reject_invalid_values() -> None:
    with pytest.raises(TypeError, match="viscosity"):
        UserDefinedProperties(
            viscosity=cast(Any, None),
            specific_heat=3000.0,
            density=1000.0,
            conductivity=0.3,
        )

    with pytest.raises(TypeError, match="freeze_point"):
        UserDefinedProperties(
            viscosity=0.002,
            specific_heat=3000.0,
            density=1000.0,
            conductivity=0.3,
            freeze_point=cast(Any, None),
        )


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_user_defined_fluid_checks_temperature_limits() -> None:
    fluid = make_user_defined_fluid(
        viscosity=lambda temp: temp,
        specific_heat=1.0,
        density=1.0,
        conductivity=1.0,
        t_min=0.0,
        t_max=10.0,
    )

    assert fluid.viscosity(-10.0) == pytest.approx(0.0)
    assert fluid.viscosity(20.0) == pytest.approx(10.0)


def test_user_defined_fluid_rejects_invalid_temperature_limits() -> None:
    with pytest.raises(ValueError, match="t_min is greater than t_max"):
        make_user_defined_fluid(t_min=10.0, t_max=10.0)


def test_user_defined_fluid_rejects_invalid_concentration_limits() -> None:
    fluid = make_user_defined_fluid()

    with pytest.raises(ValueError, match="x_min is greater than x_max"):
        fluid._set_concentration_limits(0.5, 0.6, 0.4)


def test_user_defined_fluid_checks_concentration_limits() -> None:
    fluid = make_user_defined_fluid()
    fluid._set_concentration_limits(0.5, 0.2, 0.8)

    with pytest.warns(UserWarning, match="concentration must be greater"):
        assert fluid._check_concentration(0.1) == pytest.approx(0.2)

    with pytest.warns(UserWarning, match="concentration must be less"):
        assert fluid._check_concentration(0.9) == pytest.approx(0.8)

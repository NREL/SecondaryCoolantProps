import pytest

from scp.ethyl_alcohol import EthylAlcohol


@pytest.fixture
def ea(request) -> EthylAlcohol:
    return EthylAlcohol(request.param)


@pytest.mark.parametrize(
    ("ea", "temp_c", "viscosity", "density", "specific_heat", "conductivity"),
    [
        # EthylAlcohol = 0.0
        (0.0, 5, 1.5015e-03, 1.0001e03, 4.2052e03, 5.709e-01),
        (0.0, 20, 1.0005e-03, 9.9818e02, 4.1683e03, 5.9802e-01),
        (0.0, 40, 6.5457e-04, 9.9244e02, 4.2005e03, 6.3014e-01),
        # EthylAlcohol = 0.2
        (0.2, 5, 4.0621e-03, 9.7442e02, 4.3595e03, 4.5243e-01),
        (0.2, 20, 2.1648e-03, 9.6892e02, 4.3287e03, 4.6631e-01),
        (0.2, 40, 1.164e-03, 9.5881e02, 4.32e03, 4.844e-01),
        # EthylAlcohol = 0.4
        (0.4, 5, 5.5016e-03, 9.4601e02, 3.9315e03, 3.5458e-01),
        (0.4, 20, 2.8758e-03, 9.3532e02, 4.0293e03, 3.612e-01),
        (0.4, 40, 1.4573e-03, 9.2026e02, 4.1199e03, 3.6934e-01),
    ],
    indirect=("ea",),
)
def test_properties(
    ea: EthylAlcohol,
    temp_c: float,
    viscosity: float,
    density: float,
    specific_heat: float,
    conductivity: float,
) -> None:
    # Error tolerance: 0.1%
    assert ea.viscosity(temp_c) == pytest.approx(viscosity, rel=0.001)
    assert ea.density(temp_c) == pytest.approx(density, rel=0.001)
    assert ea.specific_heat(temp_c) == pytest.approx(specific_heat, rel=0.001)
    assert ea.conductivity(temp_c) == pytest.approx(conductivity, rel=0.001)


@pytest.mark.parametrize(
    ("ea", "freeze_point"),
    [
        (0.1, -4.379),
        (0.2, -11.119),
        (0.3, -20.14),
        (0.4, -29.533),
        (0.5, -37.611),
        (0.6, -44.91),
    ],
)
def test_freeze_point(ea: float, freeze_point: float) -> None:
    # Error tolerance: 0.01C
    assert EthylAlcohol(ea).freeze_point(ea) == pytest.approx(freeze_point, abs=0.01)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_out_of_range_temps() -> None:
    ea = EthylAlcohol(0.4)
    assert ea.density(-50) == pytest.approx(ea.density(ea.t_min), abs=0.01)
    assert ea.density(150) == pytest.approx(ea.density(ea.t_max), abs=0.01)

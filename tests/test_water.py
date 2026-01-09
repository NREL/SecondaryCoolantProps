import pytest

from scp.water import Water


@pytest.fixture
def water() -> Water:
    return Water()


@pytest.mark.parametrize(
    ("temp_c", "expected"),
    [
        (1.0, 1.731e-03),
        (5.0, 1.518e-03),
        (10.0, 1.306e-03),
        (25.0, 8.9e-04),
        (50.0, 5.465e-04),
        (75.0, 3.774e-04),
        (90.0, 3.142e-04),
        (95.0, 2.971e-04),
        (99.0, 2.846e-04),
    ],
)
def test_viscosity(water: Water, temp_c: float, expected: float) -> None:
    # Error tolerance: 1.0%
    assert water.viscosity(temp_c) == pytest.approx(expected, rel=0.01)


@pytest.mark.parametrize(
    ("temp_c", "expected"),
    [
        (1.0, 4.216e03),
        (5.0, 4.205e03),
        (10.0, 4.195e03),
        (25.0, 4.181e03),
        (50.0, 4.181e03),
        (75.0, 4.193e03),
        (90.0, 4.205e03),
        (95.0, 4.21e03),
        (99.0, 4.215e03),
    ],
)
def test_specific_heat(water: Water, temp_c: float, expected: float) -> None:
    # Error tolerance: 1.0%
    assert water.specific_heat(temp_c) == pytest.approx(expected, rel=0.01)


@pytest.mark.parametrize(
    ("temp_c", "expected"),
    [
        (1.0, 9.999e02),
        (5.0, 1.0e03),
        (10.0, 9.997e02),
        (25.0, 9.97e02),
        (50.0, 9.88e02),
        (75.0, 9.748e02),
        (90.0, 9.653e02),
        (95.0, 9.619e02),
        (99.0, 9.591e02),
    ],
)
def test_density(water: Water, temp_c: float, expected: float) -> None:
    # Error tolerance: 1.0%
    assert water.density(temp_c) == pytest.approx(expected, rel=0.01)


@pytest.mark.parametrize(
    ("temp_c", "expected"),
    [
        (1.0, 5.582e-01),
        (5.0, 5.678e-01),
        (10.0, 5.788e-01),
        (25.0, 6.065e-01),
        (50.0, 6.406e-01),
        (75.0, 6.636e-01),
        # PropsSI("L", "P", 101325, "T", 273.15 + 90, "WATER")
        (90.0, 6.728e-01),
        (95.0, 6.752e-01),
        (99.0, 6.768e-01),
    ],
)
def test_conductivity(water: Water, temp_c: float, expected: float) -> None:
    # Error tolerance: 1.0%
    assert water.conductivity(temp_c) == pytest.approx(expected, rel=0.01)


def test_t_freeze(water: Water):
    # Error tolerance: 1.0%
    assert water.freeze_point() == pytest.approx(0.0, rel=0.01)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_out_of_range_temps(water: Water):
    assert water.density(-10) == pytest.approx(water.density(water.t_min), abs=0.01)
    assert water.density(110) == pytest.approx(water.density(water.t_max), abs=0.01)

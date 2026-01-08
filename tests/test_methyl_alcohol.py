import pytest

from scp.methyl_alcohol import MethylAlcohol


@pytest.fixture
def ma(request) -> MethylAlcohol:
    return MethylAlcohol(request.param)


@pytest.mark.parametrize(
    ("ma", "temp_c", "viscosity", "density", "specific_heat", "conductivity"),
    [
        # MethylAlcohol = 0.0
        (0.0, 5, 1.5169e-03, 1.0e03, 4.2159e03, 5.7057e-01),
        (0.0, 20, 1.0e-03, 9.9841e02, 4.1649e03, 5.9834e-01),
        (0.0, 40, 6.5422e-04, 9.9216e02, 4.1802e03, 6.2986e-01),
        # MethylAlcohol = 0.2
        (0.2, 5, 2.6531e-03, 9.7135e02, 4.0832e03, 4.6748e-01),
        (0.2, 20, 1.5979e-03, 9.6679e02, 4.1101e03, 4.8339e-01),
        (0.2, 40, 9.4179e-04, 9.5837e02, 4.098e03, 5.0402e-01),
        # MethylAlcohol = 0.4
        (0.4, 5, 3.0165e-03, 9.4305e02, 3.7171e03, 3.7833e-01),
        (0.4, 20, 1.8385e-03, 9.3457e02, 3.8224e03, 3.8571e-01),
        (0.4, 40, 1.0684e-03, 9.2227e02, 3.8728e03, 3.9646e-01),
    ],
    indirect=("ma",),
)
def test_properties(
    ma: MethylAlcohol,
    temp_c: float,
    viscosity: float,
    density: float,
    specific_heat: float,
    conductivity: float,
) -> None:
    # Error tolerance: 0.1%
    assert ma.viscosity(temp_c) == pytest.approx(viscosity, rel=0.001)
    assert ma.density(temp_c) == pytest.approx(density, rel=0.001)
    assert ma.specific_heat(temp_c) == pytest.approx(specific_heat, rel=0.001)
    assert ma.conductivity(temp_c) == pytest.approx(conductivity, rel=0.001)


@pytest.mark.parametrize(
    ("ma", "freeze_point"),
    [
        (0.1, -6.54),
        (0.2, -15.08),
        (0.3, -25.685),
        (0.4, -38.703),
        (0.5, -54.466),
        (0.6, -73.006),
    ],
)
def test_freeze_point(ma: float, freeze_point: float) -> None:
    # Error tolerance: 0.01C
    assert MethylAlcohol(ma).freeze_point(ma) == pytest.approx(freeze_point, abs=0.01)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_out_of_range_temps() -> None:
    ma = MethylAlcohol(0.4)
    assert ma.density(-50) == pytest.approx(ma.density(ma.t_min), abs=0.01)
    assert ma.density(150) == pytest.approx(ma.density(ma.t_max), abs=0.01)

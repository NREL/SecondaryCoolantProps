import pytest

from scp.ethylene_glycol import EthyleneGlycol


@pytest.fixture
def eg(request) -> EthyleneGlycol:
    return EthyleneGlycol(request.param)


@pytest.mark.parametrize(
    ("eg", "temp_c", "viscosity", "density", "specific_heat", "conductivity"),
    [
        # EthyleneGlycol = 0.0
        (0.0, 5, 1.5186e-03, 9.9915e02, 4.2027e03, 5.7137e-01),
        (0.0, 20, 1.0078e-03, 9.9735e02, 4.1862e03, 5.9913e-01),
        (0.0, 40, 6.5721e-04, 9.9181e02, 4.1785e03, 6.2983e-01),
        # EthyleneGlycol = 0.2
        (0.2, 5, 2.6594e-03, 1.0281e03, 3.8695e03, 4.9022e-01),
        (0.2, 20, 1.6624e-03, 1.0241e03, 3.8962e03, 5.0766e-01),
        (0.2, 40, 1.0133e-03, 1.0164e03, 3.9328e03, 5.2908e-01),
        # EthyleneGlycol = 0.4
        (0.4, 5, 4.7569e-03, 1.0585e03, 3.4559e03, 4.1376e-01),
        (0.4, 20, 2.8191e-03, 1.0519e03, 3.519e03, 4.253e-01),
        (0.4, 40, 1.6351e-03, 1.0414e03, 3.5978e03, 4.405e-01),
    ],
    indirect=("eg",),
)
def test_properties(
    eg: EthyleneGlycol,
    temp_c: float,
    viscosity: float,
    density: float,
    specific_heat: float,
    conductivity: float,
) -> None:
    # Error tolerance: 0.1%
    assert eg.viscosity(temp_c) == pytest.approx(viscosity, rel=0.001)
    assert eg.density(temp_c) == pytest.approx(density, rel=0.001)
    assert eg.specific_heat(temp_c) == pytest.approx(specific_heat, rel=0.001)
    assert eg.conductivity(temp_c) == pytest.approx(conductivity, rel=0.001)


@pytest.mark.parametrize(
    ("eg", "freeze_point"),
    [
        (0.1, -3.357),
        (0.2, -7.949),
        (0.3, -14.576),
        (0.4, -23.813),
        (0.5, -35.994),
        (0.6, -51.201),
    ],
)
def test_freeze_point(eg: float, freeze_point: float) -> None:
    # Error tolerance: 0.01C
    assert EthyleneGlycol(eg).freeze_point(eg) == pytest.approx(freeze_point, abs=0.01)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_out_of_range_temps() -> None:
    eg = EthyleneGlycol(0.4)
    assert eg.density(-50) == pytest.approx(eg.density(eg.t_min), abs=0.01)
    assert eg.density(150) == pytest.approx(eg.density(eg.t_max), abs=0.01)

import pytest

from scp.propylene_glycol import PropyleneGlycol


@pytest.fixture
def pg(request) -> PropyleneGlycol:
    return PropyleneGlycol(request.param)


@pytest.mark.parametrize(
    ("pg", "temp_c", "viscosity", "density", "specific_heat", "conductivity"),
    [
        # PropyleneGlycol = 0.0
        (0.0, 5, 1.5364e-03, 1.0003e03, 4.2048e03, 5.7124e-01),
        (0.0, 20, 1.0072e-03, 9.9852e02, 4.1866e03, 5.9913e-01),
        (0.0, 40, 6.5033e-04, 9.9253e02, 4.1783e03, 6.3007e-01),
        # PropyleneGlycol = 0.2
        (0.2, 5, 3.4941e-03, 1.0191e03, 3.9459e03, 4.7647e-01),
        (0.2, 20, 2.0301e-03, 1.0148e03, 3.9768e03, 4.9221e-01),
        (0.2, 40, 1.1693e-03, 1.0064e03, 4.0190e03, 5.1228e-01),
        # PropyleneGlycol = 0.4
        (0.4, 5, 8.9817e-03, 1.0401e03, 3.6580e03, 3.9089e-01),
        (0.4, 20, 4.3838e-03, 1.0323e03, 3.7067e03, 4.0026e-01),
        (0.4, 40, 2.1408e-03, 1.0201e03, 3.7708e03, 4.1321e-01),
    ],
    indirect=("pg",),
)
def test_properties(
    pg: PropyleneGlycol,
    temp_c: float,
    viscosity: float,
    density: float,
    specific_heat: float,
    conductivity: float,
) -> None:
    # Error tolerance: 0.1%
    assert pg.viscosity(temp_c) == pytest.approx(viscosity, rel=0.001)
    assert pg.density(temp_c) == pytest.approx(density, rel=0.001)
    assert pg.specific_heat(temp_c) == pytest.approx(specific_heat, rel=0.001)
    assert pg.conductivity(temp_c) == pytest.approx(conductivity, rel=0.001)


@pytest.mark.parametrize(
    ("pg", "freeze_point"),
    [
        (0.1, -2.867),
        (0.2, -7.173),
        (0.3, -12.789),
        (0.4, -20.568),
        (0.5, -32.193),
        (0.6, -50.003),
    ],
)
def test_freeze_point(pg: float, freeze_point: float) -> None:
    # Error tolerance: 0.01C
    assert PropyleneGlycol(pg).freeze_point(pg) == pytest.approx(freeze_point, abs=0.01)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_out_of_range_temps() -> None:
    pg = PropyleneGlycol(0.4)
    assert pg.density(-50) == pytest.approx(pg.density(pg.t_min), abs=0.01)
    assert pg.density(150) == pytest.approx(pg.density(pg.t_max), abs=0.01)

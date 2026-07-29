User-Facing API
===============

The recommended programmatic interface is the small API exposed from ``scp``.
It lets applications construct fluids and evaluate properties without importing
the concrete fluid classes directly.

Examples::

    from scp import get_fluid

    water = get_fluid("water")
    water_density = water.density(25.0)

    pg = get_fluid("propylene_glycol", concentration=0.4)
    pg_viscosity = pg.viscosity(20.0)

User-defined fluids can be created through the same API.  The core properties
can be constants or callables that accept temperature in Celsius::

    from scp import get_fluid

    fluid = get_fluid(
        "user_defined",
        name="CustomFluid",
        viscosity=lambda temp: 0.003 - 1.0e-5 * temp,
        specific_heat=3200.0,
        density=lambda temp: 1000.0 - 0.5 * temp,
        conductivity=0.42,
        freeze_point=-12.0,
        t_min=-20.0,
        t_max=80.0,
    )

    print(fluid.density(20.0))

.. automodule:: scp.api
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

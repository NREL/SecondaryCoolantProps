Preferred Programmatic Usage
============================

For programmatic usage, the preferred approach is the user-facing API exposed
from ``scp``.  Applications of using the CLI approach with ``scprop`` should be
limited to that use case.

An example usage::

    from scp import get_fluid

    class MyClass:
        def __init__(self):
            self.my_fluid = get_fluid("water")

        def do_something(self):
            # do some calculations
            # ...

            # get fluid properties
            temp = 20  # Celsius
            visc = self.my_fluid.viscosity(temp)
            dens = self.my_fluid.density(temp)

            # continue
            # ...

Other fluids can also be created through the same function.

Other examples::

    from scp import get_fluid

    ethyl_alcohol = get_fluid("ethyl_alcohol", concentration=0.3)
    ethylene_glycol = get_fluid("ethylene_glycol", concentration=0.3)
    methyl_alcohol = get_fluid("methyl_alcohol", concentration=0.3)
    propylene_glycol = get_fluid("propylene_glycol", concentration=0.3)

    water = get_fluid("water")
    density = water.density(25.0)

User-defined fluid properties can be supplied through the same API.  Constant
values are accepted, and temperature-dependent values can be callables that
accept temperature in Celsius::

    from scp import get_fluid

    custom_fluid = get_fluid(
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

    viscosity = custom_fluid.viscosity(20.0)

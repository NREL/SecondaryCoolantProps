Preferred Programmatic Usage
============================

For programmatic usage, the preferred approach is for users to directly consume
the fluid classes directly in your applications. Applications of using the CLI
approach with ``scprop`` should be limited to that use case.

An example usage::

    from scp.water import Water

    class MyClass:
        def __init__(self):
            self.my_fluid = Water()

        def do_something(self):
            # do some calculations
            # ...

            # get fluid properties
            temp = 20  # Celsius
            visc = self.my_fluid.viscosity(temp)
            dens = self.my_fluid.density(temp)

            # continue
            # ...

Other fluids can also be imported and applied in a similar fashion.

Other examples::

    from scp.ethyl_alcohol import EthylAlcohol
    from scp.ethylene_glycol import EthyleneGlycol
    from scp.methyl_alcohol import MethylAlcohol
    from scp.propylene_glycol import PropyleneGlycol

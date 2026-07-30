Water
=====

Provides fluid properties for liquid water between 0-100 C.

.. include:: _available_properties.inc

Example::

    from scp import get_fluid

    if __name__ == "__main__":
        water = get_fluid("water")

        temp = 10.0  # Celsius
        viscosity = water.viscosity(temp)
        density = water.density(temp)
        specific_heat = water.specific_heat(temp)
        conductivity = water.conductivity(temp)
        prandtl = water.prandtl(temp)
        thermal_diffusivity = water.thermal_diffusivity(temp)
        freeze_point = water.freeze_point()

        print(f"Viscosity: {viscosity} {water.viscosity_units()}")
        print(f"Density: {density} {water.density_units()}")
        print(f"Specific heat: {specific_heat} {water.specific_heat_units()}")
        print(f"Conductivity: {conductivity} {water.conductivity_units()}")
        print(f"Prandtl number: {prandtl} {water.prandtl_units()}")
        print(f"Thermal diffusivity: {thermal_diffusivity} {water.thermal_diffusivity_units()}")
        print(f"Freeze point: {freeze_point} {water.freeze_point_units()}")

.. automodule:: scp.water
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

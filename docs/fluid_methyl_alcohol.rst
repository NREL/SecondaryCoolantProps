Methyl Alcohol
==============

Provides fluid properties for aqueous mixtures of Methyl Alcohol for temperatures <= 40 C, with concentrations from 0-0.6.

.. include:: _available_properties.inc

Example::

    from scp import get_fluid

    if __name__ == "__main__":
        concentration = 0.2  # mixture concentration fraction
        methyl_alcohol = get_fluid("methyl_alcohol", concentration=concentration)

        temp = 10.0  # Celsius
        viscosity = methyl_alcohol.viscosity(temp)
        density = methyl_alcohol.density(temp)
        specific_heat = methyl_alcohol.specific_heat(temp)
        conductivity = methyl_alcohol.conductivity(temp)
        prandtl = methyl_alcohol.prandtl(temp)
        thermal_diffusivity = methyl_alcohol.thermal_diffusivity(temp)
        freeze_point = methyl_alcohol.freeze_point(concentration)

        print(f"Viscosity: {viscosity} {methyl_alcohol.viscosity_units()}")
        print(f"Density: {density} {methyl_alcohol.density_units()}")
        print(f"Specific heat: {specific_heat} {methyl_alcohol.specific_heat_units()}")
        print(f"Conductivity: {conductivity} {methyl_alcohol.conductivity_units()}")
        print(f"Prandtl number: {prandtl} {methyl_alcohol.prandtl_units()}")
        print(
            f"Thermal diffusivity: {thermal_diffusivity} "
            f"{methyl_alcohol.thermal_diffusivity_units()}"
        )
        print(f"Freeze point: {freeze_point} {methyl_alcohol.freeze_point_units()}")

.. automodule:: scp.methyl_alcohol
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Ethyl Alcohol
=============

Provides fluid properties for aqueous mixtures of Ethyl Alcohol for temperatures <= 40 C, with concentrations from 0-0.6.

.. include:: _available_properties.inc

Example::

    from scp import get_fluid

    if __name__ == "__main__":
        concentration = 0.2  # mixture concentration fraction
        ethyl_alcohol = get_fluid("ethyl_alcohol", concentration=concentration)

        temp = 10.0  # Celsius
        viscosity = ethyl_alcohol.viscosity(temp)
        density = ethyl_alcohol.density(temp)
        specific_heat = ethyl_alcohol.specific_heat(temp)
        conductivity = ethyl_alcohol.conductivity(temp)
        prandtl = ethyl_alcohol.prandtl(temp)
        thermal_diffusivity = ethyl_alcohol.thermal_diffusivity(temp)
        freeze_point = ethyl_alcohol.freeze_point(concentration)

        print(f"Viscosity: {viscosity} {ethyl_alcohol.viscosity_units()}")
        print(f"Density: {density} {ethyl_alcohol.density_units()}")
        print(f"Specific heat: {specific_heat} {ethyl_alcohol.specific_heat_units()}")
        print(f"Conductivity: {conductivity} {ethyl_alcohol.conductivity_units()}")
        print(f"Prandtl number: {prandtl} {ethyl_alcohol.prandtl_units()}")
        print(
            f"Thermal diffusivity: {thermal_diffusivity} "
            f"{ethyl_alcohol.thermal_diffusivity_units()}"
        )
        print(f"Freeze point: {freeze_point} {ethyl_alcohol.freeze_point_units()}")

.. automodule:: scp.ethyl_alcohol
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Ethylene Glycol
===============

Provides fluid properties for aqueous mixtures of Ethylene Glycol for temperatures <= 100 C, with concentrations from 0-0.6.

.. include:: _available_properties.inc

Example::

    from scp import get_fluid

    if __name__ == "__main__":
        concentration = 0.2  # mixture concentration fraction
        ethylene_glycol = get_fluid("ethylene_glycol", concentration=concentration)

        temp = 10.0  # Celsius
        viscosity = ethylene_glycol.viscosity(temp)
        density = ethylene_glycol.density(temp)
        specific_heat = ethylene_glycol.specific_heat(temp)
        conductivity = ethylene_glycol.conductivity(temp)
        prandtl = ethylene_glycol.prandtl(temp)
        thermal_diffusivity = ethylene_glycol.thermal_diffusivity(temp)
        freeze_point = ethylene_glycol.freeze_point(concentration)

        print(f"Viscosity: {viscosity} {ethylene_glycol.viscosity_units()}")
        print(f"Density: {density} {ethylene_glycol.density_units()}")
        print(f"Specific heat: {specific_heat} {ethylene_glycol.specific_heat_units()}")
        print(f"Conductivity: {conductivity} {ethylene_glycol.conductivity_units()}")
        print(f"Prandtl number: {prandtl} {ethylene_glycol.prandtl_units()}")
        print(
            f"Thermal diffusivity: {thermal_diffusivity} "
            f"{ethylene_glycol.thermal_diffusivity_units()}"
        )
        print(f"Freeze point: {freeze_point} {ethylene_glycol.freeze_point_units()}")

.. automodule:: scp.ethylene_glycol
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

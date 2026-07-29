Propylene Glycol
================

Provides fluid properties for aqueous mixtures of Propylene Glycol for temperatures <= 100 C, with concentrations from 0-0.6.

Example::

    from scp import get_fluid

    if __name__ == "__main__":
        concentration = 0.2  # mixture concentration fraction
        propylene_glycol = get_fluid("propylene_glycol", concentration=concentration)

        temp = 10.0  # Celsius
        viscosity = propylene_glycol.viscosity(temp)
        density = propylene_glycol.density(temp)
        specific_heat = propylene_glycol.specific_heat(temp)
        conductivity = propylene_glycol.conductivity(temp)
        prandtl = propylene_glycol.prandtl(temp)
        thermal_diffusivity = propylene_glycol.thermal_diffusivity(temp)
        freeze_point = propylene_glycol.freeze_point(concentration)

        print(f"Viscosity: {viscosity} {propylene_glycol.viscosity_units()}")
        print(f"Density: {density} {propylene_glycol.density_units()}")
        print(f"Specific heat: {specific_heat} {propylene_glycol.specific_heat_units()}")
        print(f"Conductivity: {conductivity} {propylene_glycol.conductivity_units()}")
        print(f"Prandtl number: {prandtl} {propylene_glycol.prandtl_units()}")
        print(
            f"Thermal diffusivity: {thermal_diffusivity} "
            f"{propylene_glycol.thermal_diffusivity_units()}"
        )
        print(f"Freeze point: {freeze_point} {propylene_glycol.freeze_point_units()}")

.. automodule:: scp.propylene_glycol
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

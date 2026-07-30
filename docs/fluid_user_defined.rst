User-Defined Fluid
==================

Provides a fluid implementation where applications supply the core property
values directly.  Prefer creating this fluid with ``scp.get_fluid("user_defined", ...)``.
Viscosity, specific heat, density, and conductivity are required.  Each property
can be a constant value or a callable that accepts temperature in Celsius.
Freeze point is optional and defaults to 0 C.

.. include:: _available_properties.inc

Example with inline property values::

    from scp import get_fluid

    if __name__ == "__main__":
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

        temp = 20.0  # Celsius
        viscosity = custom_fluid.viscosity(temp)
        density = custom_fluid.density(temp)
        specific_heat = custom_fluid.specific_heat(temp)
        conductivity = custom_fluid.conductivity(temp)
        prandtl = custom_fluid.prandtl(temp)
        thermal_diffusivity = custom_fluid.thermal_diffusivity(temp)
        freeze_point = custom_fluid.freeze_point()

        print(f"Viscosity: {viscosity} {custom_fluid.viscosity_units()}")
        print(f"Density: {density} {custom_fluid.density_units()}")
        print(f"Specific heat: {specific_heat} {custom_fluid.specific_heat_units()}")
        print(f"Conductivity: {conductivity} {custom_fluid.conductivity_units()}")
        print(f"Prandtl number: {prandtl} {custom_fluid.prandtl_units()}")
        print(f"Thermal diffusivity: {thermal_diffusivity} {custom_fluid.thermal_diffusivity_units()}")
        print(f"Freeze point: {freeze_point} {custom_fluid.freeze_point_units()}")

Example using a reusable property object::

    from scp import UserDefinedProperties, get_fluid

    properties = UserDefinedProperties(
        viscosity=0.002,
        specific_heat=3200.0,
        density=1050.0,
        conductivity=0.42,
        freeze_point=-12.0,
    )

    custom_fluid = get_fluid(
        "user_defined",
        name="CustomFluid",
        properties=properties,
        t_min=-20.0,
        t_max=80.0,
    )

.. automodule:: scp.user_defined
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

from sys import stderr

import click

from scp.api import available_fluids, available_properties, get_fluid

# Add this to .bashrc for nice completion: eval "$(_SCPROP_COMPLETE=bash_source scprop)"

fluid_options = click.Choice(available_fluids(include_user_defined=False))
prop_options = click.Choice(available_properties())
x_range = click.FloatRange(min=0.0, max=1.0)


@click.command(name="SecondaryCoolantPropsCommandLine")
@click.option(
    "-f",
    "--fluid",
    type=fluid_options,
    required=True,
    default="water",
    help="Which fluid to use?",
)
@click.option(
    "-x",
    "--concentration",
    type=x_range,
    required=False,
    default=0.0,
    help="Mixture concentration fraction. Default 0.0.",
)
@click.option(
    "-p",
    "--property",
    "fluid_prop",
    type=prop_options,
    required=True,
    help="Which fluid property to evaluate.",
)
@click.option(
    "-t",
    "--temperature",
    type=float,
    required=True,
    help="Fluid temperature, in degrees Celsius.",
)
@click.option(
    "-q",
    "--quick",
    is_flag=True,
    show_default=True,
    default=False,
    help="Just report the value, good for scripts",
)
def cli(fluid: str, concentration: float, fluid_prop: str, temperature: float, quick: bool):
    if concentration == 0.0 and fluid != "water":
        print(
            "Mixture requested, but concentration zero, assuming water and continuing",
            file=stderr,
        )
    elif concentration > 0.0 and fluid == "water":
        print(
            "Pure water requested, but nonzero concentration entered, assuming water and continuing",
            file=stderr,
        )
    if fluid == "water" or concentration == 0.0:
        f = get_fluid("water")
        fluid = "water"
    else:
        f = get_fluid(fluid, concentration=concentration)

    if fluid_prop == "freeze_point":
        value = getattr(f, fluid_prop)(concentration)
    else:
        value = getattr(f, fluid_prop)(temperature)
    units = getattr(f, f"{fluid_prop}_units")()
    if quick:
        print(value)
    else:
        print(f"Fluid:    {fluid}\nProperty: {fluid_prop}\nValue:    {value}\nUnits:    [{units}]")

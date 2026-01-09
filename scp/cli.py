from sys import stderr

import click

from scp import ethyl_alcohol, ethylene_glycol, methyl_alcohol, propylene_glycol, water

# Add this to .bashrc for nice completion: eval "$(_SCPROP_COMPLETE=bash_source scprop)"

fluids = {
    "water": water.Water,
    "ethyl_alcohol": ethyl_alcohol.EthylAlcohol,
    "ethylene_glycol": ethylene_glycol.EthyleneGlycol,
    "methyl_alcohol": methyl_alcohol.MethylAlcohol,
    "propylene_glycol": propylene_glycol.PropyleneGlycol,
}
fluid_options = click.Choice(list(fluids.keys()))
properties = (
    "viscosity",
    "specific_heat",
    "density",
    "conductivity",
    "prandtl",
    "thermal_diffusivity",
    "freeze_point",
)
prop_options = click.Choice(properties)
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
        f = water.Water()
        fluid = "water"
    else:
        f = fluids[fluid](concentration)

    if fluid_prop == "freeze_point":
        value = getattr(f, fluid_prop)(concentration)
    else:
        value = getattr(f, fluid_prop)(temperature)
    units = getattr(f, f"{fluid_prop}_units")()
    if quick:
        print(value)
    else:
        print(f"Fluid:    {fluid}\nProperty: {fluid_prop}\nValue:    {value}\nUnits:    [{units}]")

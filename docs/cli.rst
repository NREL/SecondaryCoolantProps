Command Line Usage
==================

This library comes with a command line interface.
Once this library is pip installed, a new binary executable will be available with the name ``scprop``.
The command has a help argument with output similar to this (execute manually to verify latest syntax)::

    $ scprop --help
    Usage: scprop [OPTIONS]

    Options:
      -f, --fluid [water|ethyl_alcohol|ethylene_glycol|methyl_alcohol|propylene_glycol]
                                      Which fluid to use?  [required]
      -x, --concentration FLOAT RANGE
                                      Mixture concentration fraction. Default 0.0.
                                      [0.0<=x<=1.0]
      -p, --property [viscosity|specific_heat|density|conductivity|prandtl|thermal_diffusivity|freeze_point]
                                      Which fluid property to evaluate.
                                      [required]
      -t, --temperature FLOAT         Fluid temperature, in degrees Celsius.
                                      [required]
      -q, --quick                     Just report the value, good for scripts
      --help                          Show this message and exit.

Some example usages::

    $ scprop --fluid water --property density --temperature 25
    Fluid:    water
    Property: density
    Value:    997.0448954179155
    Units:    [kg/m3]

    $ scprop --fluid water --property density --temperature 25 --quick
    997.0448954179155

    $ scprop --fluid ethylene_glycol --concentration 0.3 --property specific_heat --temperature 40
    Fluid:    ethylene_glycol
    Property: specific_heat
    Value:    3775.3537088494118
    Units:    [J/kg-K]

Note that the fluid argument must be from the list of supported fluids, and the property must be from the list of supported properties.
Both of these are available from the help message.
For glycol mixtures, the glycol concentration is a decimal value.
The temperature input value is in Celsius.

By default the output is a nice summary, but there is a quick option that just reports the value.
The quick value is a nice integration into some workflows that would require the CLI.

For interactive bash sessions, there is a tab-completion capability available.
Simply add the following line to the ``.bashrc`` file, or execute it manually in the current session to apply it temporarily::

    eval "$(_SCPROP_COMPLETE=bash_source scprop)"

Enabling this will turn on tab completion for the different argument names, as well as the supported fluid and property names.

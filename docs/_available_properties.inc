Available Properties
--------------------

Each fluid instance exposes these property methods:

.. list-table::
   :header-rows: 1
   :widths: 30 24 18 18

   * - Property
     - Method
     - Alias
     - Units
   * - Dynamic viscosity
     - ``viscosity(temp)``
     - ``mu(temp)``
     - ``Pa-s``
   * - Specific heat
     - ``specific_heat(temp)``
     - ``cp(temp)``
     - ``J/kg-K``
   * - Density
     - ``density(temp)``
     - ``rho(temp)``
     - ``kg/m3``
   * - Thermal conductivity
     - ``conductivity(temp)``
     - ``k(temp)``
     - ``W/m-K``
   * - Prandtl number
     - ``prandtl(temp)``
     - ``pr(temp)``
     - ``-``
   * - Thermal diffusivity
     - ``thermal_diffusivity(temp)``
     - ``alpha(temp)``
     - ``m2/s``
   * - Freezing point
     - ``freeze_point(x)``
     -
     - ``C``

Temperature arguments are in degrees Celsius.  For mixture fluids,
``freeze_point(x)`` uses concentration fraction ``x``.  For water and
constant user-defined freezing points, ``freeze_point()`` can be called
without a concentration.

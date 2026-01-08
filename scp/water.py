from scp.base_fluid import BaseFluid


class Water(BaseFluid):
    def __init__(self) -> None:
        """
        This class represents water as a fluid.  The constructor
        does not require any arguments for the pure water fluid.
        """
        super().__init__(0.0, 100.0)

    @property
    def fluid_name(self) -> str:
        """
        Returns the fluid name for this derived fluid.
        @return: "Water"
        """
        return "Water"

    def viscosity(self, temp: float) -> float:
        """
        Returns the viscosity of water.

        @param temp: Fluid temperature, in degrees Celsius
        @return: The dynamic viscosity of water in [Pa-s]
        """

        temp = self._check_temperature(temp)

        am0 = -3.30233
        am1 = 1301
        am2 = 998.333
        am3 = 8.1855
        am4 = 0.00585
        am5 = 1.002
        am6 = -1.3272
        am7 = -0.001053
        am8 = 105
        am10 = 0.68714
        am11 = -0.0059231
        am12 = 2.1249e-05
        am13 = -2.69575e-08

        if temp < 20:
            exponent = am0 + am1 / (am2 + (temp - 20) * (am3 + am4 * (temp - 20)))
            return (10**exponent) * 0.1
        if temp > 100:
            return (am10 + temp * am11 + (temp**2) * am12 + (temp**3) * am13) * 0.001
        return (am5 * 10 ** ((temp - 20) * (am6 + (temp - 20) * am7) / (temp + am8))) * 0.001

    def specific_heat(self, temp: float) -> float:
        """
        Returns the fluid specific heat.

        Specific heat of water at 1 atmosphere, 0 to 100 C.  Equation from linear least-squares
        regression of data from CRC Handbook (op.cit.) page D-174

        @param temp: Fluid temperature, in degrees Celsius
        @return: Specific heat, in [J/kg-K]
        """

        temp = self._check_temperature(temp)

        acp0 = 4.21534
        acp1 = -0.00287819
        acp2 = 7.4729e-05
        acp3 = -7.79624e-07
        acp4 = 3.220424e-09

        return (acp0 + temp * acp1 + (temp**2) * acp2 + (temp**3) * acp3 + (temp**4) * acp4) * 1000

    def freeze_point(self, _=None) -> float:
        """
        Returns the freezing point temperature of water

        @param _: Unused variable
        @return Freezing point temperature, in Celsius
        """
        return 0.0

    def conductivity(self, temp: float) -> float:
        """
        Returns the fluid thermal conductivity for this derived fluid.

        Thermal conductivity equation from linear least-squares fit to data in CRC Handbook (op.cit.), page E-11

        @param temp: Fluid temperature, in degrees Celsius
        @return: Thermal conductivity, in [W/m-K]
        """

        temp = self._check_temperature(temp)

        ak0 = 0.560101
        ak1 = 0.00211703
        ak2 = -1.05172e-05
        ak3 = 1.497323e-08
        ak4 = -1.48553e-11

        return ak0 + temp * ak1 + (temp**2) * ak2 + (temp**3) * ak3 + (temp**4) * ak4

    def density(self, temp: float) -> float:
        """
        Returns the fluid density for this derived fluid.

        Density eq. for water at 1 atm., from CRC Handbook of Chem. & Phys., 61st Edition (1980-1981), p. F-6.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Density, in [kg/m3]
        """

        temp = self._check_temperature(temp)

        ar0 = 999.83952
        ar1 = 16.945176
        ar2 = -0.0079870401
        ar3 = -4.6170461e-05
        ar4 = 1.0556302e-07
        ar5 = -2.8054253e-10
        ar6 = 0.01687985

        return (ar0 + temp * ar1 + (temp**2) * ar2 + (temp**3) * ar3 + (temp**4) * ar4 + (temp**5) * ar5) / (
            1 + ar6 * temp
        )

from abc import abstractmethod
from math import exp

from scp.base_fluid import BaseFluid

# Ideally the type hints would cause the coefficient returns to return this, but it is
#  bulky and I haven't been able to get a new typing NewType to work properly, so for now
#  they just return a plain Tuple.
# Tuple[
#     Tuple[float, float, float, float],
#     Tuple[float, float, float, float],
#     Tuple[float, float, float, float],
#     Tuple[float, float, float],
#     Tuple[float, float],
#     float
# ]


class BaseMelinder(BaseFluid):
    """
    A base class for Melinder fluids that provides convenience methods
    that can be accessed in derived classes.

    Melinder, Å. 2010. Properties of Secondary Working Fluids
    for Indirect Systems. 2nd ed. International Institute of Refrigeration.
    """

    _ij_pairs = (
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
        (5, 0),
    )

    @abstractmethod
    def coefficient_freezing(self) -> tuple:
        """
        Abstract method; derived classes should override to return the
        coefficient matrix for freezing point.
        """

    @abstractmethod
    def coefficient_viscosity(self) -> tuple:
        """
        Abstract method; derived classes should override to return the
        coefficient matrix for viscosity.
        """

    @abstractmethod
    def coefficient_specific_heat(self) -> tuple:
        """
        Abstract method; derived classes should override to return the
        coefficient matrix for specific heat.
        """

    @abstractmethod
    def coefficient_conductivity(self) -> tuple:
        """
        Abstract method; derived classes should override to return the
        coefficient matrix for conductivity.
        """

    @abstractmethod
    def coefficient_density(self) -> tuple:
        """
        Abstract method; derived classes should override to return the
        coefficient matrix for density.
        """

    def __init__(
        self,
        t_min: float,
        t_max: float,
        x: float,
        x_min: float,
        x_max: float,
    ):
        """
        A constructor for the Melinder fluid base class

        @param t_min: Minimum temperature, in degrees Celsius
        @param t_max: Maximum temperature, in degrees Celsius
        @param x: Concentration fraction, from 0 to 1
        @param x_min: Minimum concentration fraction, from 0 to 1
        @param x_max: Maximum concentration fraction, from 0 to 1
        """

        super().__init__(t_min, t_max, x, x_min, x_max)
        self.x_base: float | None = None
        self.t_base: float | None = None

    def _f_prop_t_freeze(self, c_arr: tuple, x: float) -> float:
        """
        General worker function to evaluate fluid properties as
        a function of concentration.

        @param c_arr:
        @param x:

        @return:
        """

        if self.x_base is None:
            raise ValueError("x_base is not set")
        if self.t_base is None:
            raise ValueError("t_base is not set")

        x = self._check_concentration(x)

        xxm = (x * 100) - self.x_base
        yym = self.t_base
        x_xm = [xxm**p for p in range(6)]
        y_ym = [yym**p for p in range(4)]

        f_ret = 0.0

        for i, j in BaseMelinder._ij_pairs:
            f_ret += c_arr[i][j] * x_xm[i] * y_ym[j]

        return f_ret

    def _f_prop(self, c_arr: tuple, temp: float) -> float:
        """
        General worker function to evaluate fluid properties as
        a function of concentration and temperature.

        @param c_arr:
        @param temp:

        @return:
        """

        if self.x_base is None:
            raise ValueError("x_base is not set")
        if self.t_base is None:
            raise ValueError("t_base is not set")

        temp = self._check_temperature(temp)

        xxm = self.x_pct - self.x_base
        yym = temp - self.t_base
        x_xm = [xxm**p for p in range(6)]
        y_ym = [yym**p for p in range(4)]

        f_ret = 0.0

        for i, j in BaseMelinder._ij_pairs:
            f_ret += c_arr[i][j] * x_xm[i] * y_ym[j]

        return f_ret

    def viscosity(self, temp: float) -> float:
        """
        Calculate the dynamic viscosity of the mixture

        @param temp: Fluid temperature, in degrees Celsius
        @return: Dynamic viscosity, in N/m2-s, or Pa-s
        """

        return exp(self._f_prop(self.coefficient_viscosity(), temp)) / 1000.0

    def specific_heat(self, temp: float) -> float:
        """
        Calculates the specific heat of the mixture

        @param temp: Fluid temperature, in degrees Celsius
        @return: Specific heat, in J/kg-K
        """

        return self._f_prop(self.coefficient_specific_heat(), temp)

    def conductivity(self, temp: float) -> float:
        """
        Calculates the thermal conductivity of the mixture

        @param temp: Fluid temperature, in degrees Celsius
        @return: Thermal conductivity, in W/m-K
        """

        return self._f_prop(self.coefficient_conductivity(), temp)

    def density(self, temp: float) -> float:
        """
        Calculates the density of the mixture

        @param temp: Fluid temperature, in degrees Celsius
        @return: Density, in kg/m3
        """

        return self._f_prop(self.coefficient_density(), temp)

    def freeze_point(self, x: float) -> float:
        """
        Calculate the freezing point temperature of the mixture

        @param x: Concentration fraction
        @return Freezing point temperature, in Celsius
        """

        return self._f_prop_t_freeze(self.coefficient_freezing(), x)

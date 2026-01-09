import warnings
from abc import ABC, abstractmethod


class BaseFluid(ABC):
    """
    A fluid base class that provides convenience methods that can be accessed
    in derived classes.
    """

    def __init__(
        self,
        t_min: float,
        t_max: float,
        x: float | None = None,
        x_min: float | None = None,
        x_max: float | None = None,
    ):
        """
        A constructor for a base fluid, that takes a concentration as an argument.
        Derived classes can decide how to handle the concentration argument and
        their own constructor interface as needed to construct and manage that
        specific derived class.

        @param t_min: Minimum temperature, in degrees Celsius
        @param t_max: Maximum temperature, in degrees Celsius
        @param x: Concentration fraction, from 0 to 1
        @param x_min: Minimum concentration fraction, from 0 to 1
        @param x_max: Maximum concentration fraction, from 0 to 1
        """

        self._set_temperature_limits(t_min, t_max)

        if isinstance(x, float) and isinstance(x_min, float) and isinstance(x_max, float):
            self._set_concentration_limits(x, x_min, x_max)

    @property
    @abstractmethod
    def fluid_name(self) -> str:
        """
        An abstract property that needs to return the fluid name in derived fluid classes

        Derived function must be decorated with @property

        @return: string name of the fluid
        """

    def _set_concentration_limits(self, x: float, x_min: float, x_max: float):
        """
        An internal worker function that checks the given concentration against limits,
        and sets internal variables.

        @param x: The concentration fraction to check, ranging from 0 to 1
        @param x_min: The minimum concentration fraction to allow, ranging from 0 to 1
        @param x_max: The maximum concentration fraction to allow, ranging from 0 to 1
        @return: Nothing
        """

        if x_min >= x_max:
            msg = f'Developer error: Fluid "{self.fluid_name}", x_min is greater than x_max'
            raise ValueError(msg)

        self.x_min = x_min
        self.x_max = x_max
        self.x = self._check_concentration(x)
        self.x_pct = self.x * 100

    def _check_concentration(self, x: float) -> float:
        """
        An internal worker function that checks the given concentration against limits

        @param x: The concentration to check, in percent
        @return: A validated concentration value, in percent
        """

        if x < self.x_min:
            msg = f'Fluid "{self.fluid_name}", concentration must be greater than {self.x_min:0.2f}.\n'
            msg += f"Resetting concentration to {self.x_min:0.2f}."
            warnings.warn(msg)
            return self.x_min
        elif x > self.x_max:
            msg = f'Fluid "{self.fluid_name}", concentration must be less than {self.x_max:0.2f}.\n'
            msg += f"Resetting concentration to {self.x_max:0.2f}."
            warnings.warn(msg)
            return self.x_max
        else:
            return x

    def _set_temperature_limits(self, t_min, t_max) -> None:
        """
        A worker function to override the default temperature min/max values

        @param t_min: The minimum temperature value to allow, in degrees Celsius
        @param t_max: The maximum temperature value to allow, in degrees Celsius
        @return: Nothing
        """

        if t_min >= t_max:
            msg = f'Fluid "{self.fluid_name}", t_min is greater than t_max'
            raise ValueError(msg)

        self.t_min = t_min
        self.t_max = t_max

    def _check_temperature(self, temp: float) -> float:
        """
        An internal worker function that checks the given temperature against limits

        @param temp: The temperature to check, in degrees Celsius
        @return: A validated temperature value, in degrees Celsius
        """

        if temp < self.t_min:
            msg = f'Fluid "{self.fluid_name}", temperature must be greater than {self.t_min:0.1f}.\n'
            msg += f"Resetting temperature to {self.t_min:0.1f}."
            warnings.warn(msg)
            return self.t_min
        elif temp > self.t_max:
            msg = f'Fluid "{self.fluid_name}", temperature must be less than {self.t_max:0.1f}.\n'
            msg += f"Resetting temperature to {self.t_max:0.1f}."
            warnings.warn(msg)
            return self.t_max
        else:
            return temp

    @abstractmethod
    def freeze_point(self, x: float) -> float:
        """
        Abstract method; derived classes should override the freezing
        point of that fluid

        @param x: Fluid concentration fraction, ranging from 0 to 1
        @return Returns the freezing point of the fluid, in Celsius
        """

    @staticmethod
    def freeze_point_units() -> str:
        return "C"

    @abstractmethod
    def viscosity(self, temp: float) -> float:
        """
        Abstract method; derived classes should override to return the dynamic
        viscosity of that fluid.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the dynamic viscosity in [Pa-s]
        """

    @staticmethod
    def viscosity_units() -> str:
        return "Pa-s"

    def mu(self, temp: float) -> float:
        """
        Convenience function for returning the dynamic viscosity by the common letter 'mu'

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the dynamic viscosity -- which one is mu in [Pa-s]
        """
        return self.viscosity(temp)

    @abstractmethod
    def specific_heat(self, temp: float) -> float:
        """
        Abstract method; derived classes should override to return the specific heat
        of that fluid.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the specific heat in [J/kg-K]
        """

    @staticmethod
    def specific_heat_units() -> str:
        return "J/kg-K"

    def cp(self, temp: float) -> float:
        """
        Convenience function for returning the specific heat by the common shorthand 'cp'

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the specific heat in [J/kg-K]
        """
        return self.specific_heat(temp)

    @abstractmethod
    def density(self, temp: float) -> float:
        """
        Abstract method; derived classes should override to return the density
        of that fluid.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the density in [kg/m3]
        """

    @staticmethod
    def density_units() -> str:
        return "kg/m3"

    def rho(self, temp: float) -> float:
        """
        Convenience function for returning the density by the common shorthand 'rho'

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the density, in [kg/m3]
        """
        return self.density(temp)

    @abstractmethod
    def conductivity(self, temp: float) -> float:
        """
        Abstract method; derived classes should override to return the thermal
        conductivity of that fluid.

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the thermal conductivity in [W/m-K]
        """

    @staticmethod
    def conductivity_units() -> str:
        return "W/m-K"

    def k(self, temp: float) -> float:
        """
        Convenience function for returning the thermal conductivity by the common shorthand 'k'

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the thermal conductivity, in [W/m-K]
        """
        return self.conductivity(temp)

    def prandtl(self, temp: float) -> float:
        """
        Returns the Prandtl number for this fluid

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the dimensionless Prandtl number
        """
        return self.cp(temp) * self.mu(temp) / self.k(temp)

    @staticmethod
    def prandtl_units() -> str:
        return "-"

    def pr(self, temp: float = 0.0) -> float:
        """
        Convenience function for returning the Prandtl number by the common shorthand 'pr'

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the dimensionless Prandtl number
        """
        return self.prandtl(temp)

    def thermal_diffusivity(self, temp: float) -> float:
        """
        Returns the thermal diffusivity for this fluid

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the thermal diffusivity in [m2/s]
        """
        return self.k(temp) / (self.rho(temp) * self.cp(temp))

    @staticmethod
    def thermal_diffusivity_units() -> str:
        return "m2/s"

    def alpha(self, temp: float) -> float:
        """
        Convenience function for returning the thermal diffusivity by the common shorthand 'alpha'

        @param temp: Fluid temperature, in degrees Celsius
        @return: Returns the thermal diffusivity in [m2/s]
        """
        return self.thermal_diffusivity(temp)

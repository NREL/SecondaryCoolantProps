from scp.base_melinder import BaseMelinder


class EthyleneGlycol(BaseMelinder):
    """
    A derived fluid class for ethylene glycol and water mixtures
    """

    def coefficient_freezing(self) -> tuple:
        return (
            (-1.5250e01, -1.5660e-06, -2.2780e-07, 2.1690e-09),
            (-8.0800e-01, -1.3390e-06, 2.0470e-08, -2.7170e-11),
            (-1.3340e-02, 6.3220e-08, 2.3730e-10, -2.1830e-12),
            (-7.2930e-05, 1.7640e-09, -2.4420e-11),
            (1.0060e-06, -7.6620e-11),
            (1.1400e-09,),
        )

    def coefficient_viscosity(self) -> tuple:
        return (
            (4.7050e-01, -2.5500e-02, 1.7820e-04, -7.6690e-07),
            (2.4710e-02, -1.1710e-04, 1.0520e-06, -1.6340e-08),
            (3.3280e-06, 1.0860e-06, 1.0510e-08, -6.4750e-10),
            (1.6590e-06, 3.1570e-09, 4.0630e-10),
            (3.0890e-08, 1.8310e-10),
            (-1.8650e-09,),
        )

    def coefficient_specific_heat(self) -> tuple:
        return (
            (3.7370e03, 2.9300e00, -4.6750e-03, -1.3890e-05),
            (-1.7990e01, 1.0460e-01, -4.1470e-04, 1.8470e-7),
            (-9.9330e-02, 3.5160e-04, 5.1090e-06, -7.1380e-08),
            (2.6100e-03, -1.1890e-06, -1.6430e-7),
            (1.5370e-05, -4.2720e-07),
            (-1.6180e-06,),
        )

    def coefficient_conductivity(self) -> tuple:
        return (
            (4.7200e-01, 8.9030e-04, -1.0580e-06, -2.7890e-09),
            (-4.2860e-03, -1.4730e-05, 1.0590e-07, -1.1420e-10),
            (1.7470e-05, 6.8140e-08, -3.6120e-09, 2.3650e-12),
            (3.0170e-08, -2.4120e-09, 4.0040e-11),
            (-1.3220e-09, 2.5550e-11),
            (2.6780e-11,),
        )

    def coefficient_density(self) -> tuple:
        return (
            (1.0340e03, -4.7810e-01, -2.6920e-03, 4.7250e-06),
            (1.3110e00, -6.8760e-03, 4.8050e-05, 1.6900e-08),
            (7.4900e-05, 7.8550e-05, -3.9950e-07, 4.9820e-09),
            (-1.0620e-04, 1.2290e-06, -1.1530e-08),
            (-9.6230e-07, -7.2110e-08),
            (4.8910e-08,),
        )

    def __init__(self, x: float) -> None:
        """
        Constructor for an ethylene glycol mixture instance

        @param x: Concentration fraction, from 0 to 0.6
        """

        super().__init__(0.0, 100, x, 0.0, 0.6)
        self.x_base = 30.8462
        self.t_base = 31.728
        self.t_min = self.t_freeze = self.freeze_point(x)

    @property
    def fluid_name(self) -> str:
        """
        Returns a descriptive title for this fluid
        @return: "EthyleneGlycol"
        """
        return "EthyleneGlycol"

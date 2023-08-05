from .util import Status


class Inverter:
    def __init__(
        self,
        id: int,
        name: str,
        sn: str,
        total_energy: float,
        today_energy: float,
        power_factor: float,
        frequency: float,
        power: float,
        status: Status,
        temperature: int,
    ) -> None:
        self.id = id
        self.name = name
        self.sn = sn
        self.total_energy = total_energy
        self.today_energy = today_energy
        self.power_factor = power_factor
        self.frequency = frequency
        self.power = power
        self.status = status
        self.temperature = temperature
        self.phases: list[Phase] = []
        self.mppts: list[MPPT] = []

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


class Phase:
    def __init__(
        self,
        name: str,
        voltage: float,
        amperage: float,
        status_voltage: Status,
        status_amperage: Status,
    ) -> None:
        self.name = name
        self.voltage = voltage
        self.amperage = amperage
        self.status_voltage = status_voltage
        self.status_amperage = status_amperage

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


class MPPT:
    def __init__(self, name: str) -> None:
        self.name = name
        self.strings: list[String] = []

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)


class String:
    def __init__(
        self, name: str, voltage: float, amperage: float, status: Status
    ) -> None:
        self.name = name
        self.voltage = voltage
        self.amperage = amperage
        self.status = status

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

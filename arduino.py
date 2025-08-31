import sys, serial
from sqlalchemy import case, false, true

from main import zone

class Arduino:
    def __init__(self, port: str = "", baudRate: int = 9600) -> none:
        self.baudRate = baudRate
        if port != "":
            self.port = port
        else:
            self.port = self.selectPort()
        self.coms = serial.Serial(self.port, baudrate=self.baudRate, timeout=.1)

    def write(tent_light_letter: str, zone_name: str, object_letter, enable: bool) -> none:

        match zone_name:
            case "archipelago":
                zone_letter = "A"
            case "deepSeas":
                zone_letter = "D"
            case "roughSeas":
                zone_letter = "W"
            case "volcanoe":
                zone_letter = "V"
            case "navy":
                zone_letter = "N"

        if enable:
            enable_letter = "e"
        else:
            enable_letter = "d"

        message = tent_light_letter + zone_letter + object_letter + enable_letter
        self.coms.write(message.encode('utf-8'))
        self.coms.write(bytes('\n', encoding='utf-8'))


    def selectPort() -> none:
        ports = serial.tools.list_ports.comports()
        validPorts = [port for port in ports if port.hwid != 'n/a']

        if not validPorts:
            raise NoValidPortError("No valid Arduino ports found.")

        print('PORT\tDEVICE\t\t\tMANUFACTURER')
        for index, value in enumerate(sorted(validPorts)):
            print(f"{index}\t{value.name}\t{value.manufacturer}")

        choice = -1
        while choice < 0 or choice >= len(validPorts):
            answer = input("➜ Select your port: ")
            if answer.isnumeric():
                choice = int(answer)

        selectedPort = sorted(validPorts)[choice]
        print(f"selecting: {selectedPort.device}")
        return selectedPort.device

# arduinos: dict[arduino] = {"map": none, "kraken": none, "skyAnimation": none, "atmosphere": none, "zombies": none, "roughSeas": none, "volcanoe": none, "navy": none}
main_arduino = Arduino("COM6", 9600)

def update_lights(zone_name: str, state: str) -> none:
    match state:
        case "normal":
            main_arduino.write("l", zone_name, "k", false)
            main_arduino.write("l", zone_name, "t", false)
            main_arduino.write("l", zone_name, "z", false)
        case "goldenHour":
            main_arduino.write("l", zone_name, "k", false)
            main_arduino.write("l", zone_name, "t", true)
            main_arduino.write("l", zone_name, "z", false)
        case "zombiePirates":
            main_arduino.write("l", zone_name, "k", false)
            main_arduino.write("l", zone_name, "t", false)
            main_arduino.write("l", zone_name, "z", true)
        case "kraken":
            main_arduino.write("l", zone_name, "k", true)
            main_arduino.write("l", zone_name, "t", false)
            main_arduino.write("l", zone_name, "z", false)
        case "zombieKraken":
            main_arduino.write("l", zone_name, "k", true)
            main_arduino.write("l", zone_name, "t", false)
            main_arduino.write("l", zone_name, "z", true)
        case "goldenZombie":
            main_arduino.write("l", zone_name, "k", false)
            main_arduino.write("l", zone_name, "t", true)
            main_arduino.write("l", zone_name, "z", true)
        case "goldenKraken":
            main_arduino.write("l", zone_name, "k", true)
            main_arduino.write("l", zone_name, "t", true)
            main_arduino.write("l", zone_name, "z", false)
        case "goldenZombieKraken":
            main_arduino.write("l", zone_name, "k", true)
            main_arduino.write("l", zone_name, "t", true)
            main_arduino.write("l", zone_name, "z", true)

def update_tentacles(zone_name: str, state: str) -> none:
    match state:
        case "normal":
            main_arduino.write("t", zone_name, "0", false)
        case "goldenHour":
            main_arduino.write("t", zone_name, "0", false)
        case "zombiePirates":
            main_arduino.write("t", zone_name, "0", false)
        case "kraken":
            main_arduino.write("t", zone_name, "0", true)
        case "zombieKraken":
            main_arduino.write("t", zone_name, "0", true)
        case "goldenZombie":
            main_arduino.write("t", zone_name, "0", false)
        case "goldenKraken":
            main_arduino.write("t", zone_name, "0", true)
        case "goldenZombieKraken":
            main_arduino.write("t", zone_name, "0", true)

class NoValidPortError(Exception):
    """Exception raised when no valid Arduino ports are found."""
    pass

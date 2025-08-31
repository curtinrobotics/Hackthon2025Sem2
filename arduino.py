import sys, serial
#from sqlalchemy import case, False, True

class Arduino:
    def __init__(self, port: str = "", baudRate: int = 9600) -> None:
        self.baudRate = baudRate
        if port != "":
            self.port = port
        else:
            self.port = self.selectPort()
        self.coms = serial.Serial(self.port, baudrate=self.baudRate, timeout=.1)

    def write(self, tent_light_letter: str, zone_name: str, object_letter, enable: bool) -> None:
        zone_letter = "A"
        enable_letter = "d"
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


    def selectPort() -> None:
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

# arduinos: dict[arduino] = {"map": None, "kraken": None, "skyAnimation": None, "atmosphere": None, "zombies": None, "roughSeas": None, "volcanoe": None, "navy": None}

main_arduino = Arduino("COM16", 9600)

def update_lights(zone_name: str, state: str) -> None:
    match state:
        case "normal":
            main_arduino.write("l", zone_name, "k", False)
            main_arduino.write("l", zone_name, "t", False)
            main_arduino.write("l", zone_name, "z", False)
        case "goldenHour":
            main_arduino.write("l", zone_name, "k", False)
            main_arduino.write("l", zone_name, "t", True)
            main_arduino.write("l", zone_name, "z", False)
        case "zombiePirates":
            main_arduino.write("l", zone_name, "k", False)
            main_arduino.write("l", zone_name, "t", False)
            main_arduino.write("l", zone_name, "z", True)
        case "kraken":
            main_arduino.write("l", zone_name, "k", True)
            main_arduino.write("l", zone_name, "t", False)
            main_arduino.write("l", zone_name, "z", False)
        case "zombieKraken":
            main_arduino.write("l", zone_name, "k", True)
            main_arduino.write("l", zone_name, "t", False)
            main_arduino.write("l", zone_name, "z", True)
        case "goldenZombie":
            main_arduino.write("l", zone_name, "k", False)
            main_arduino.write("l", zone_name, "t", True)
            main_arduino.write("l", zone_name, "z", True)
        case "goldenKraken":
            main_arduino.write("l", zone_name, "k", True)
            main_arduino.write("l", zone_name, "t", True)
            main_arduino.write("l", zone_name, "z", False)
        case "goldenZombieKraken":
            main_arduino.write("l", zone_name, "k", True)
            main_arduino.write("l", zone_name, "t", True)
            main_arduino.write("l", zone_name, "z", True)

def update_tentacles(zone_name: str, state: str) -> None:
    match state:
        case "normal":
            main_arduino.write("t", zone_name, "0", False)
        case "goldenHour":
            main_arduino.write("t", zone_name, "0", False)
        case "zombiePirates":
            main_arduino.write("t", zone_name, "0", False)
        case "kraken":
            main_arduino.write("t", zone_name, "0", True)
        case "zombieKraken":
            main_arduino.write("t", zone_name, "0", True)
        case "goldenZombie":
            main_arduino.write("t", zone_name, "0", False)
        case "goldenKraken":
            main_arduino.write("t", zone_name, "0", True)
        case "goldenZombieKraken":
            main_arduino.write("t", zone_name, "0", True)

class NoValidPortError(Exception):
    """Exception raised when no valid Arduino ports are found."""
    pass

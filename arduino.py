import sys, serial

arduinos: dict[arduino] = {"map": none, "kraken": none, "skyAnimation": none, "atmosphere": none, "zombies": none, "roughSeas": none, "volcanoe": none, "navy": none}

def update(name: str, zone: str, object: str, command: str) -> none:
    arduinos[name].write(zone, object, command)

def setup() -> none:
    for device in arduinos:
        arduinos[device] = arduino(device)

class NoValidPortError(Exception):
    """Exception raised when no valid Arduino ports are found."""
    pass

class arduino:
    def __init__(name: str, port: str = "", baudRate: int = 9600) -> none:
        self.name = name
        self.baudRate = baudRate
        if port != "":
            self.port = port
        else:
            self.port = self.selectPort()
        self.coms = serial.Serial(self.port, baudrate=self.baudRate, timeout=.1)

    def write(zone: str, object: str, command: str) -> none:
        message = "[" + zone + "|" + object "|" + command + "]"
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

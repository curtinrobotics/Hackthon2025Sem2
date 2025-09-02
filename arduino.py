import sys, serial
import time
import threading
#from sqlalchemy import case, False, True

class Arduino:
    def __init__(self, port: str = "", baudRate: int = 9600) -> None:
        self.baudRate = baudRate
        if port != "":
            self.port = port
        else:
            self.port = self.selectPort()
        self.coms = serial.Serial(self.port, baudrate=self.baudRate, timeout=.1)

    def write(self, tent_light_letter: str, zone_name: str, object_letter, enable: str) -> None:
        zone_letter = "_"
        enable_letter = "_"
        match zone_name:
            case "archipelago":
                zone_letter = "A"
            case "deepSeas":
                zone_letter = "D"
            case "roughSeas":
                zone_letter = "W"
            case "volcano":
                zone_letter = "V"
            case "navy":
                zone_letter = "N"

        message = tent_light_letter + zone_letter + object_letter + enable_letter
        print(f"Sending to arduino:|{message}|", end="")

        self.coms.write(message.encode('utf-8'))
        print("...", end="")
        time.sleep(0.01)
        #self.coms.write(bytes('\n', encoding='utf-8'))
        print("Done")


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

arduino_port = "COM6"
print("Using port " + arduino_port)
print("Assigned on line 63 in arduino.py")
main_arduino = Arduino(arduino_port, 9600)

def blink_lights(zone_name: str, state: str) -> None:
    threads = []
    match state:
        case "normal":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "d")
        case "goldenhour":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "b")
            #main_arduino.write("l", zone_name, "z", "d")
        case "zombiepirates":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "b",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "b")
        case "kraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "b")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "d")
        case "zombiekraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "b",)))
            #main_arduino.write("l", zone_name, "k", "b")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "b")
        case "goldenzombie":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "b",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "b")
            #main_arduino.write("l", zone_name, "z", "b")
        case "goldenkraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "b")
            #main_arduino.write("l", zone_name, "t", "b")
            #main_arduino.write("l", zone_name, "z", "d")
        case "goldenzombiekraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "b",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "b",)))
            #main_arduino.write("l", zone_name, "k", "b")
            #main_arduino.write("l", zone_name, "t", "b")
            #main_arduino.write("l", zone_name, "z", "b")
    for thread in threads:
        thread.start()
        time.sleep(0.01)

def update_lights(zone_name: str, state: str) -> None:
    state = state.lower()
    threads = []
    match state:
        case "normal":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "d")
        case "goldenhour":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "e")
            #main_arduino.write("l", zone_name, "z", "d")
        case "zombiepirates":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "e",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "e")
        case "kraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "e")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "d")
        case "zombiekraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "e",)))
            #main_arduino.write("l", zone_name, "k", "e")
            #main_arduino.write("l", zone_name, "t", "d")
            #main_arduino.write("l", zone_name, "z", "e")
        case "goldenzombie":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "d",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "e",)))
            #main_arduino.write("l", zone_name, "k", "d")
            #main_arduino.write("l", zone_name, "t", "e")
            #main_arduino.write("l", zone_name, "z", "e")
        case "goldenkraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "d",)))
            #main_arduino.write("l", zone_name, "k", "e")
            #main_arduino.write("l", zone_name, "t", "e")
            #main_arduino.write("l", zone_name, "z", "d")
        case "goldenzombiekraken":
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "k", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "t", "e",)))
            threads.append(threading.Thread(target=main_arduino.write, args=("l", zone_name, "z", "e",)))
            #main_arduino.write("l", zone_name, "k", "e")
            #main_arduino.write("l", zone_name, "t", "e")
            #main_arduino.write("l", zone_name, "z", "e")
    for thread in threads:
        thread.start()
        time.sleep(0.01)

def update_tentacles(zone_name: str, state: str) -> None:
    state = state.lower()
    match state:
        case "normal":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "d",))
            #main_arduino.write("t", zone_name, "0", "d")
        case "goldenhour":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "d",))
            #main_arduino.write("t", zone_name, "0", "d")
        case "zombiepirates":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "d",))
            #main_arduino.write("t", zone_name, "0", "d")
        case "kraken":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "e",))
            #main_arduino.write("t", zone_name, "0", "e")
        case "zombiekraken":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "e",))
            #main_arduino.write("t", zone_name, "0", "e")
        case "goldenzombie":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "d",))
            #main_arduino.write("t", zone_name, "0", "d")
        case "goldenkraken":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "e",))
            #main_arduino.write("t", zone_name, "0", "e")
        case "goldenzombiekraken":
            thread = threading.Thread(target=main_arduino.write, args=("t", zone_name, "0", "e",))
            #main_arduino.write("t", zone_name, "0", "e")
    thread.start()
    time.sleep(0.01)

class NoValidPortError(Exception):
    """Exception raised when no valid Arduino ports are found."""
    pass

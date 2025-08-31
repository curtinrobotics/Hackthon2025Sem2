from main import zone
class roughSeas(zone):
    def __init__(name: str = "roughSeas", krakaenArms: list[int], motorPort: int = 9, speed: int = 5) -> None:
        self.motorPort = motorPort
        self.speed = speed
        super().__init__(name, krakaenArms)

    def audio(filename: str) -> None:
        match filename:
            case: "gail":
                filename = filename + str(random(5))
        super().audio(filename)

    def animation(ani: str) -> None:
        case "rollingSeas":
            rollingSeas(self.speed)
        case _:
            super().animation(ani)

    def rollingSeas() -> None:
        if self.speed >= 8:
            lightningCrash()
        elif self.speed >= 6:
            rollingLighning()
        elif self.speed >= 4:
            gail()
        arduino.update(self.name, self.name, str(self.motorPort), str(self.speed))


    def gail() -> None:
        audio("gail")

    def updateSpeed(speed: int) -> None:
        self.speed = speed
        self.animation(rollingSeas)

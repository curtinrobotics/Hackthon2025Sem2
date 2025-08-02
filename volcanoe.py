from main import zone
class volcanoe(zone):
    def __init__(name: str = "volcanoe", krakaenArms: list[int]) -> none:
        super.__init__(name, krakaenArms)

    def audio(filename: str) -> none:
        match filename:
            case: "erruption":
                filename = filename + str(random(5))
        super().audio(filename)

    def animation(ani: str) -> none:
        case "lavaFlow":
            lavaFlow()
        case "smokeOn":
            smoke("On"):
        case "smokeOff":
            smoke("Off"):
        case "erruption":
            erruption()
        case _:
            super().animation(ani)

    def erruption(delay: int = 10000) -> none:
        audio("erruption")
        smoke("On")
        arduino.update("volcanoe", self.name, "lava", "spew")
        time.sleep(delay)
        lavaFlow()

    def lavaFLow() -> none:
        smoke("Off")
        arduino.update("volcanoe", self.name, "lava", "spew")

    def smoke(state: str) -> none:
        arduino.update("volcanoe", self.name, "smoke", state)

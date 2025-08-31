from main import zone
class volcanoe(zone):
    def __init__(name: str = "volcanoe", krakaenArms: list[int]) -> None:
        super.__init__(name, krakaenArms)

    def audio(filename: str) -> None:
        match filename:
            case: "erruption":
                filename = filename + str(random(5))
        super().audio(filename)

    def animation(ani: str) -> None:
        match ani:
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

    def erruption(delay: int = 10000) -> None:
        audio("erruption")
        smoke("On")
        arduino.update("volcanoe", self.name, "lava", "spew")
        time.sleep(delay)
        lavaFlow()

    def lavaFLow() -> None:
        smoke("Off")
        arduino.update("volcanoe", self.name, "lava", "spew")

    def smoke(state: str) -> None:
        arduino.update("volcanoe", self.name, "smoke", state)

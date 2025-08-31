from main import zone
class navy(zone):
    def __init__(name: str = "navy", krakaenArms: list[int], cannons: list[int] = [1, 2, 3]) -> None:
        self.cannons = cannons
        super.__init__(name, krakaenArms)

    def audio(filename: str) -> None:
        match filename:
            case: "cannonFire":
                filename = filename + str(random(5))
        super().audio(filename)

    def animation(ani: str) -> None:
        case "Fire":
            fire(random(len(cannons)))
        case _:
            super().animation(ani)

    def fire(cannon) -> None:
        arduino.update("navy", self.name, "cannon", cannons[cannon])

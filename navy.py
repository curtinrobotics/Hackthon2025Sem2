from main import zone
class navy(zone):
    def __init__(name: str = "navy", krakaenArms: list[int], cannons: list[int] = [1, 2, 3]) -> none:
        self.cannons = cannons
        super.__init__(name, krakaenArms)

    def audio(filename: str) -> none:
        match filename:
            case: "cannonFire":
                filename = filename + str(random(5))
        super().audio(filename)

    def animation(ani: str) -> none:
        case "Fire":
            fire(random(len(cannons)))
        case _:
            super().animation(ani)

    def fire(cannon) -> none:
        arduino.update("navy", self.name, "cannon", cannons[cannon])

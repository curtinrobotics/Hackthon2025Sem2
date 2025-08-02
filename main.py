from playsound import playsound
import arduino

class zone:
    def __init__(name: str, krakaenArms: list[int], currentState: str = "normal", inidcators: dict[int] = ["normal": 1, "goldenHour": 2, "zombiePirates": 3, "kraken": 4, "zombieKraken": 5]) -> none:
        self.name: str = name
        self.currentState: list[str] = currentState
        self.tentacles: list[int] = krakenArms
        self.indicators: dict[int] = indicators

    def audio(filename: str) -> none:
        match filename:
            case: "krakenInjured":
                filename = filename + str(random(5))
            case: "krakenRoar":
                filename = filename + str(random(3))
            case: "tentacleCrash":
                filename = filename + str(random(10))
            case: "heavenlyNoise":
                filename = filename
            case: "zombieGroan":
                filename = filename + str(random(10))
            case: "zombieDeath":
                filename = filename + str(random(5))
            case: "thunderCrash":
                filename = filename + str(random(5))
            case: "atmosphere":
                filename = filename + str(random(5))
            case: "ambience":
                filename = filename + str(random(5))
            case: "thunderCrash":
                filename = filename
            case: "thunderRoll":
                filename = filename + str(random(5))
            case: "themeMusic":
                filename = filename + str(random(5))
        playsound(filename + ".mp3")

    def changeStates(states: list[str], warningTime: int = 5000) -> none:
        for state in currentState:
            if state in states:
                states.pop(state)
            else:
                changeState(state, warningTime, "off")
        for state in states:
            changeState(state, warningTime, "on")

    def changeState(state: str, warningTime: int = 5000, switch) -> none:
        match state:
            case "normal":
                changeMap(state)
            case "goldenHour":
                changeMap(state)
                time.sleep(warningTime)
                if switch == "off":
                    animation("goldenHourSets")
                elif switch == "on":
                    animation("goldenHourDawns")
            case "zombiePirates":
                changeMap(state)
                time.sleep(warningTime)
                if switch == "off":
                    animation("zombiesRise")
                elif switch == "on":
                    animation("zombiesSlumber")
            case "kraken":
                changeMap(state)
                time.sleep(warningTime)
                if switch == "off":
                    animation("krakenRetreat")
                elif switch == "on":
                    animation("krakenArise")
            case "zombieKraken":
                changeMap(state)
                time.sleep(warningTime)
                if switch == "off":
                    animation("zombieKrakenRetreat")
                elif switch == "on":
                    animation("zombieKrakenArise")
            case _:
                print("state")

    def animation(ani: str) -> none:
        match ani:
            case "tentacleWiggle":
                wiggleTentacles()
            case "tentacleSlam":
                slamTentacles()
            case "liftTentacles":
                liftTentacles()
            case "goldenHourSets":
                setGoldenHour()
            case: "goldenHourDawns":
                dawnGoldenHour()
            case: "zombiesRise":
                zombiesRise()
            case: "zombiesSlumber":
                zombiesSlumber()
            case: "krakenRetreats":
                krakenRetreats()
            case: "krakenArise":
                krakenArise()
            case: "zombieKrakenRetreat":
                zombieKrakenRetreat()
            case: "zombieKrakenArise":
                zombieKrakenArise()
            case "krakenRisesFromTheDepths":
                krakenRisesFromTheDepths()
            case "theKrakenReturns":
                theKrakenReturns()
            case "zombiesRiseFromTheDead":
                zombiesRiseFromTheDead()
            case "gameIntro":
                gameIntro()
            case "practiceIntro":
                practiceIntro()
            case "atmosphere":
                atmosphere(random(5))
            case "rollingLighning":
                rollingLighning()
            case "lightningCrash":
                lightningCrash()
            case _:
                print("unkown animation")

    #generic animations and actions
    def changeMap(state: str) -> none:
        arduino.update("map", self.name, self.indicators[state], "stateChange")

    def wiggleTentacles() -> none:
        for tentacle in self.tentacles:
            self.wiggleTentacle(tentacle)

    def wiggleTentacle(tentacle: int) -> none:
        arduino.update("kraken", self.name, tentacle, "wiggle")

    def slamTentacles(delay: int = 100) -> none:
        order: list[num] = []
        current = random(len(self.tentacles))
        order.append(current)
        for ii in range(len(self.tentacles)-2):
            while current in order:
                current = random(len(self.tentacles))
            order.append(current)
        for tentacle in self.tentacles:
            if tentacle not in order:
                order.append(tenatcle)
        for tentacle in order:
            self.slamTentacle(tentacle)
            time.sleep(delay)

    def slamTentacle(tentacle: int) -> none:
        arduino.update("kraken", self.name, tentacle, "slam")
        audio("tentacleCrash")

    def liftTentacles() -> none:
        for tentacle in self.tentacles:
            self.liftTentacle(tentacle)

    def liftTentacle(tentacle: int) -> none:
        arduino.update("kraken", self.name, tentacle, "lift")

    def TentacleChangeColour(colour: str = "purple") -> none:
        arduino.update("kraken", self.name, "colour", colour)

    def setGoldenHour(delay: int = 2000) -> none:
        arduino.update("skyAnimation", self.name, "goldenLight", "flicker")
        time.sleep(delay)
        arduino.update("skyAnimation", self.name, "goldenLight", "off")

    def dawnGoldenHour() -> none:
        arduino.update("skyAnimation", self.name, "goldenLight", "on")
        audio("heavenlyNoise")

    def zombiesRise() -> none:
        arduino.update("zombies", self.name, "zombieFigures", "up")
        arduino.update("skyAnimation", self.name, "redLight", "on")
        audio("zombieGroan")

    def zombiesSlumber() -> none:
        arduino.update("zombies", self.name, "zombieFigures", "off")
        arduino.update("skyAnimation", self.name, "redLight", "down")
        audio("zombieDeath")

    def krakenRetreats() -> none:
        wiggleTentacles()
        liftTentacles()

    def krakenArise() -> none:
        wiggleTentacles()
        audio("krakenRoar")
        slamTentacles()

    def damageKraken(tentacle: int) -> none:
        audio("krakenInjured")
        liftTentacle(tentacle)

    def zombieKrakenRetreat(delay: int = 2000) -> none:
        wiggleTentacles()
        time.sleep()
        liftTentacles()

    def zombieKrakenArise() -> none:
        wiggleTentacles()
        audio("krakenRoar")
        audio("zombieGroan")
        slamTentacles()

    #universal specific atmospheric animations
    def atmosphere(animation: str, state: str) -> none:
        arduino.update("atmosphere", self.name, animation, state)
    #story points
    def practiceIntro() -> none:
        audio("storyPracticeRun")

    def gameIntro() -> none:
        audio("gameRun")
        audio("beware")

    def zombiesRiseFromTheDead() -> none:
        audio("storyZombieRise")
        audio("zombieGroan")
        arduino.update("zombies", self.name, "zombieFigures", "up")
        arduino.update("skyAnimation", self.name, "redLight", "flash")

    def krakenRisesFromTheDepths() -> none:
        tentacleChangeColour("purple")
        wiggleTentacles()
        audio("krakenRoar")
        audio("thundercrash")
        arduino.update("skyAnimation", self.name, "lightning", "rolling")
        audio("storyKrakenRise")

    def krakenisDefeated() -> none:
        wiggleTentacles()
        audio("krakenRoar")
        audio("krakenInjured")
        liftTentacles()
        audio("storyKrakenDefeat")

    def theKrakenReturns() -> none:
        tentacleChangeColour("green")
        wiggleTentacles()
        audio("krakenRoar")
        audio("storyKrakenReturns")

    def lightningCrash() -> none:
        audio("thundercrash")
        arduino.update("skyAnimation", self.name, "lightning", "crash")

    def rollingLighning() -> none:
        audio("thunderrumble")
        arduino.update("skyAnimation", self.name, "lightning", "rolling")





#2 modes, testing mode, and play mode(big reveal, lights, sounds colours, audio, music, voic prompts)
#5 seconds ish of warning before zone change
#iniatialise all zone and game state:
#play intro music, intro audio, intro animations
#30-ish seconds of non-zones, just chill
#first zone change, ALWAYS golden zone, then zombies couple seconds later, then kraken
#2ish minutes of zones changing fairly rapidly and Normal(semi random)
#1 minute kraken dies, playzone is fairly chill, then last 10ish seconds kraken "RISES FROM THE DEAD"
#zombie kraken enters play zone
#1 min 30 ish of zombie kraken zone chasing player

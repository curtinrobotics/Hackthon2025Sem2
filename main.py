from playsound import playsound
import arduino
import random
import time
import math
import threading

class zone:
    def __init__(self, name: str, currentState: str = "normal") -> None:
        self.name: str = name
        self.currentState: str = currentState

    def audio(filename: str) -> None:
        match filename:
            case "krakenInjured":
                filename = filename + str(random(5))
            case "krakenRoar":
                filename = filename + str(random(3))
            case "tentacleCrash":
                filename = filename + str(random(10))
            case "heavenlyNoise":
                filename = filename
            case "zombieGroan":
                filename = filename + str(random(10))
            case "zombieDeath":
                filename = filename + str(random(5))
            case "thunderCrash":
                filename = filename + str(random(5))
            case "atmosphere":
                filename = filename + str(random(5))
            case "ambience":
                filename = filename + str(random(5))
            case "thunderCrash":
                filename = filename
            case "thunderRoll":
                filename = filename + str(random(5))
            case "themeMusic":
                filename = filename + str(random(5))
        playsound(filename + ".mp3")

    def animation(ani: str) -> None:
        match ani:
            case "tentacleSlam":
                slamTentacles()
            case "liftTentacles":
                liftTentacles()
            case "goldenHourSets":
                setGoldenHour()
            case "goldenHourDawns":
                dawnGoldenHour()
            case "zombiesRise":
                zombiesRise()
            case "zombiesSlumber":
                zombiesSlumber()
            case "krakenRetreats":
                krakenRetreats()
            case "krakenArise":
                krakenArise()
            case "zombieKrakenRetreat":
                zombieKrakenRetreat()
            case "zombieKrakenArise":
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

    def changeBoard(self) -> None:
        arduino.update_tentacles(self.name, self.currentState)

    #generic animations and actions
    def changeMap(self, newState) -> None:
        arduino.update_lights(self.name, newState)

    def warningMap(self, state: str) -> None:
        arduino.blink_lights(self.name, state)

def storyAnimation(story_point: str) -> None:
    match story_point:
        case "start":
            print("start\n")
            #playsound("start.mp3")
        case "zombiesRise":
            print("zombiesRise\n")
            playsound("zombiesRise.mp3")
        case "krakenAppears":
            print("krakenAppears\n")
            #playsound("krakenAppears.mp3")
        case "krakenRises":
            print("krakenRises\n")
            playsound("krakenRises.mp3")
        case "krakenDies":
            print("krakenDies\n")
            playsound("krakenDies.mp3")
        case "zombieKrakenRises":
            print("zombieKrakenRises\n")
            playsound("zombieKrakenRises.mp3")
        case"zombieKrakenDies":
            print("zombieKrakenDies\n")
            playsound("zombieKrakenDies.mp3")
        case "finish":
            print("finish.mp3")
            #playsound("finish\n")


story_points = {
    20: "zombiesRise",
    30: "krakenAppears",
    90: "krakenRises",
    120: "krakenDies",
    160: "zombieKrakenRises",
    230: "zombieKrakenDies"
}

real_game_loop = {
    0: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    10: {
        "archipelago": "goldenHour",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    20: {
        "archipelago": "goldenHour",
        "deepSeas": "zombiePirates",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    30: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombiePirates",
        "volcano": "kraken",
        "roughSeas": "normal"
    },
    40: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "kraken",
        "roughSeas": "kraken"
    },
    50: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    60: {
        "archipelago": "kraken",
        "deepSeas": "goldenHour",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    70: {
        "archipelago": "kraken",
        "deepSeas": "normal",
        "navy": "kraken",
        "volcano": "goldenHour",
        "roughSeas": "normal"
    },
    80: {
        "archipelago": "kraken",
        "deepSeas": "normal",
        "navy": "kraken",
        "volcano": "normal",
        "roughSeas": "goldenHour"
    },
    90: {
        "archipelago": "kraken",
        "deepSeas": "kraken",
        "navy": "kraken",
        "volcano": "kraken",
        "roughSeas": "zombieKraken"
    },
    100: {
        "archipelago": "kraken",
        "deepSeas": "kraken",
        "navy": "kraken",
        "volcano": "kraken",
        "roughSeas": "goldenZombieKraken"
    },
    110: {
        "archipelago": "kraken",
        "deepSeas": "goldenKraken",
        "navy": "kraken",
        "volcano": "kraken",
        "roughSeas": "goldenKraken"
    },
    120: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    130: {
        "archipelago": "zombiePirates",
        "deepSeas": "zombiePirates",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    140: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombiePirates",
        "volcano": "normal",
        "roughSeas": "zombiePirates"
    },
    150: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "goldenHour",
        "volcano": "zombiePirates",
        "roughSeas": "normal"
    },
    160: {
        "archipelago": "zombieKraken",
        "deepSeas": "zombieKraken",
        "navy": "zombieKraken",
        "volcano": "zombieKraken",
        "roughSeas": "zombieKraken"
    },
    170: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombieKraken",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    180: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombieKraken",
        "volcano": "goldenHour",
        "roughSeas": "normal"
    },
    190: {
        "archipelago": "zombiePirates",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "zombieKraken",
        "roughSeas": "normal"
    },
    200: {
        "archipelago": "zombieKraken",
        "deepSeas": "goldenHour",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    210: {
        "archipelago": "normal",
        "deepSeas": "zombieKraken",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    220: {
        "archipelago": "goldenZombieKraken",
        "deepSeas": "normal",
        "navy": "zombieKraken",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    230: {
        "archipelago": "goldenZombieKraken",
        "deepSeas": "normal",
        "navy": "zombieKraken",
        "volcano": "zombieKraken",
        "roughSeas": "normal"
    },
    240: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "goldenHour",
        "volcano": "normal",
        "roughSeas": "normal"
    }
}

practice_game_loop = {
    0: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    10: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "goldenHour",
        "roughSeas": "normal"
    },
    20: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "zombiePirates",
        "roughSeas": "normal"
    },
    30: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombiePirates",
        "volcano": "kraken",
        "roughSeas": "normal"
    },
    40: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "kraken",
        "roughSeas": "kraken"
    },
    50: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    60: {
        "archipelago": "kraken",
        "deepSeas": "goldenHour",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    70: {
        "archipelago": "kraken",
        "deepSeas": "normal",
        "navy": "kraken",
        "volcano": "goldenHour",
        "roughSeas": "normal"
    },
    80: {
        "archipelago": "kraken",
        "deepSeas": "normal",
        "navy": "kraken",
        "volcano": "normal",
        "roughSeas": "goldenHour"
    },
    90: {
        "archipelago": "kraken",
        "deepSeas": "normal",
        "navy": "goldenZombie",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    100: {
        "archipelago": "normal",
        "deepSeas": "kraken",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    110: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "kraken",
        "volcano": "normal",
        "roughSeas": "goldenKraken"
    },
    120: {
        "archipelago": "kraken",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    130: {
        "archipelago": "zombiePirates",
        "deepSeas": "zombiePirates",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    140: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombiePirates",
        "volcano": "normal",
        "roughSeas": "zombiePirates"
    },
    150: {
        "archipelago": "zombiePirates",
        "deepSeas": "normal",
        "navy": "goldenHour",
        "volcano": "zombiePirates",
        "roughSeas": "normal"
    },
    160: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    170: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "kraken",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    180: {
        "archipelago": "normal",
        "deepSeas": "kraken",
        "navy": "kraken",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    190: {
        "archipelago": "normal",
        "deepSeas": "kraken",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "zombiePirates"
    },
    200: {
        "archipelago": "normal",
        "deepSeas": "zombiePirates",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "goldenHour"
    },
    210: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    220: {
        "archipelago": "zombieKraken",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    230: {
        "archipelago": "zombieKraken",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    240: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    }
}

test_game_loop = {
    0: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "normal",
        "roughSeas": "normal"
    },
    10: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "goldenHour",
        "roughSeas": "normal"
    },
    20: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "normal",
        "volcano": "zombiePirates",
        "roughSeas": "normal"
    },
    30: {
        "archipelago": "normal",
        "deepSeas": "normal",
        "navy": "zombiePirates",
        "volcano": "kraken",
        "roughSeas": "normal"
    }
}

zones = [zone(name) for name in ["archipelago", "deepSeas", "navy", "volcano", "roughSeas"]]


finishtime = 250 #seconds
timeGap = 10 #time between timePoints in seconds
warningTime = 5 #seconds
blinkSpeed = 0.5 #seconds
loopDelay = 0.25 #seconds
gameLoop = test_game_loop

print("Select run mode")
print("T - test game loop")
print("P - practice game loop")
print("S - real game loop")
print("R - random")
mode = input("select run mode: ").upper()

match mode:
    case "T":
        print("Selectd mode Test")
        gameLoop = test_game_loop
        finishtime = 40
    case "P":
        print("Selected mode Practice")
        gameLoop = practice_game_loop
    case "S":
        gameLoop = real_game_loop
        print("Selected mode Story")
    case _:
        print("Invalid mode selected")
        exit()

class TimerHelper:
    def __init__(self):
        self.startTime = time.time()
        self.times = []
    def addTime(self, name):
        self.times.append((name, time.time()))
    def __str__(self):
        outString = ""
        prevTime = self.startTime
        prevName = "start"
        for curName, curTime in self.times:
            outString += f" | {prevName}: {(curTime-prevTime):.4f}"
            prevTime = curTime
            prevName = curName
        return outString

startTime = time.time()
timer = 0
storyAnimation("start")
while timer < finishtime:
    loopTimer = TimerHelper()
    for timePoint in gameLoop.keys():
        if timer > timePoint + warningTime:
            for gameZone in gameLoop[timePoint].keys():
                for zone in zones:
                    if zone.name == gameZone:
                        if gameLoop[timePoint][gameZone] != zone.currentState:
                            zone.currentState = gameLoop[timePoint][gameZone]
                            zone.changeBoard()
                            zone.changeMap(zone.currentState)
        elif timer > timePoint and timer < timePoint + warningTime:
            for gameZone in gameLoop[timePoint].keys():
                for zone in zones:
                    if zone.name == gameZone:
                        if gameLoop[timePoint][gameZone] != zone.currentState:
                            zone.warningMap(gameLoop[timePoint][gameZone])

    loopTimer.addTime(f"removal{math.floor(timer)-timeGap+1}")
    for timePoint in range(0, math.floor(timer)-timeGap+1):
        if timePoint in gameLoop:
            gameLoop.pop(timePoint)
    if mode == "S":
        for timePoint in story_points.keys():
            if timer > timePoint:
                #storyAnimation(story_points[timePoint])
                animation = threading.Thread(target=storyAnimation, args=(story_points[timePoint],))
                animation.start()
        for timePoint in range(0, math.floor(timer)+1):
            if timePoint in story_points:
                story_points.pop(timePoint)
    loopTimer.addTime("end")
    time.sleep(loopDelay)
    print(f"{timer:.2f}{loopTimer}\n")
    timer = time.time() - startTime
storyAnimation("finish")
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

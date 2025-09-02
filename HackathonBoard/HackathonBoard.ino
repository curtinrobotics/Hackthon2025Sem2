// Includes
#include <Arduino.h>
#include <Servo.h>

/*
 * CRoC Hackathon 2025S2 Game Board Code
 * 
 * Contains 3 elements:
 *  - Tentacle Controller
 *    This consists of the Tentacle_t struct, which contains the IO assignment, angle configuration, 
 *    Servo instance and some state variables. An array of these classes is iterated through to update 
 *    positions and register hits. The limit switches are linked to the interupt pins (as pullups) which 
 *    trigger on the falling edge when the switch closes. These interupts flag the hit in the hits array 
 *    (if the associated tentacle is enabled) to be procesed by the main loop. 
 *    The lifecycle of a tentacle is the following: 
 *    1. The tentacle is initialised, creating the Servo instance and attaching it to the configured 
 *       pin. This also sets the pin modes. 
 *    2. The tentacle is activated by a serial message. This moves the tentacle to the configured rest 
 *       angle and sets the appropriate element of the enabled array to true. 
 *    3. The main loop reads that the tentacle is enabled and steps its motion randomly up to 10 degrees, 
 *       cycling between the min and max angle configured in the struct. The enabled output is turned on. 
 *    4. The limit switch is hit, causing the interupt to flag True in the hits array. 
 *    5. The main loop processes the tentacle and sees the hit flag. it toggles the lights to enabled off 
 *       and hit on, and stores the current time for later use. It turns off the enabled flag for the tentacle. 
 *    6. The main loop skips moving the tentacle as it is no longer enabled, leaving it stationary but 
 *       extended on the board. 
 *    7. The main loop checks the current time and sees it is > HIT_RETRACT_TIME, and disables the tentacle. 
 *       The tentacle retracts to the rest angle. 
 *    8. The main loop checks the currrent time and sees it is > HIT_LIGHT_TIME, and turns off the hit output.
 *
 *    The random may want to be replaced with a fixed step or otherwise tuned, it wasn't the smoothest motion
 *    in testing.
 *
 *  - Lighting Controller
 *    The lighting cntroller controls the lights for the active state in each zone of the board. It consists 
 *    of 5 arrays of the 3 pins the lights for each zone are connected to. Its lifecycle is to initialise the 
 *    3 pins in the array as outputs, then to setLights(ZoneArray, {'Z','K','T'} ConditionChar, BoolState) 
 *    which toggles the light for the specified pin to the requested state.
 *  - Serial Processor
 *    This function needs to be updated to match the existing serial output from the python control code. 
 *    Currently it takes a message of the following bytes:
 *    0 = {0..4} tentacle to be controlled
 *    1 = {'e', 'd'} tentacle command Enable/Disable
 *    2 = {1..5} lighting zone to be controlled
 *    3 = {'Z','K','T'} light to be controlled within the zone Zombie/Kraken/Treasure
 *    4 = {'e', 'd'} tentacle command Enable/Disable
 *
 */


// Structs
struct Tentacle_t {
	// config
	uint8_t ServoPin;  // Servo Control Pin 		(PWM out)
	uint8_t RestAng;   // Resting servo angle		(degrees)
	uint8_t MinAng;    // Min wave servo angle		(degrees)
	uint8_t MaxAng;    // Max wave servo angle 	(degrees)
	// variables
	Servo TentacleServo;  // Servo class				(Servo)
	bool Enabled;
	bool direction;    // direction of servo step  (increase/decrease)
	uint8_t position;  // current position of servo(degrees)
};


// Globals
// Tentacle Variables
int minAngle = 90;
int restAngle = 90;
int maxAngle = 165;
Tentacle_t Tentacles[10] = {
	// TODO: Configure Angles post assembly
	//|               Pins   |       Angles     |  Servo  |      |     |
	//| Servo |  Rest | Min | Max |  Class  |  Dir | Pos |
	{ 3, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TA1
	{ 4, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TA2
	{ 5, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TA3
	{ 6, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TD1
	{ 7, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TD2
	{ 8, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TN1
	{ 9, restAngle, minAngle, maxAngle, Servo(), false, 90 },   //TN2
	{ 10, restAngle, minAngle, maxAngle, Servo(), false, 90 },  //TW1
	{ 11, restAngle, minAngle, maxAngle, Servo(), false, 90 },  //TV1
	{ 12, restAngle, minAngle, maxAngle, Servo(), false, 90 }   //TV2
};

const long unsigned HIT_LIGHT_TIME = 2000;    //ms
const long unsigned HIT_RETRACT_TIME = 1000;  //ms
long unsigned nextMoveTime = 0;

// Tentacle IDs
#define tA1 0
#define tA2 1
#define tA3 2
#define tD1 3
#define tD2 4
#define tN1 5
#define tN2 6
#define tW1 7
#define tV1 8
#define tV2 9

// The below are outside the struct as the interupt interacts with them
// is tentacle enabled
//bool enabled[10] = { false, false, false, false, false, false, false, false, false, false };

// Lighting Variables
// ZoneX = {KrakenPin, ZombiePin, TreasurePin}
const uint8_t ZA[] = { 36, 37, 38 };
const uint8_t ZD[] = { 39, 40, 41 };
const uint8_t ZN[] = { 42, 43, 44 };
const uint8_t ZW[] = { 45, 46, 47 };
const uint8_t ZV[] = { 48, 49, 50 };

const uint8_t lights[][3] = {
	{ 36, 37, 38 },
	{ 39, 40, 41 },
	{ 42, 43, 44 },
	{ 45, 46, 47 },
	{ 48, 49, 50 }
};

bool blinking[][3] = {
	{ false, false, false },
	{ false, false, false },
	{ false, false, false },
	{ false, false, false },
	{ false, false, false }
};
const long unsigned BLINK_TIME = 500;
long unsigned nextBlinkTime = 0;

//Serial Variables
const int BAUD_RATE = 9600;
const int MESSAGE_BYTES = 4;
char message[MESSAGE_BYTES + 1];
/*
serial message format:

char 0: [t, l] for tentacle command or light command

for a tentacle command:
char 1: A, where A = [A, D, N, W, V] for zone name 
char 2: X, where X = [1, 2, 3] for which servo in the zone
char 3: [e, d] for enable or disable

for a light command:
char 1: A, where A = [A, D, N, W, V] for zone name 
char 2: [k, t, z] for kraken, treasure or zombie light
char 3: [e, d] for enable or disable
*/

// Function Prototypes
void InitTentacle(uint8_t iTentacle);
void Sweep(uint8_t iTentacle);
void ProcessSerial();
void ProcessTentacle(uint8_t iTentacle);
void EnableTentacle(uint8_t iTentacle);
void DisableTentacle(uint8_t iTentacle);
void MoveTentacle(uint8_t iTentacle);
void InitLights(uint8_t iPins[]);
void SetLight(uint8_t iPins[], char iType, bool iState);
void LightDemo(int times, int t);

// Main section
void setup() {
	Serial.begin(BAUD_RATE);
	for (uint8_t i = 0; i < 10; i++) {
		InitTentacle(i);
	}

	// Other Lighting
	InitLights(ZA);
	InitLights(ZD);
	InitLights(ZN);
	InitLights(ZW);
	InitLights(ZV);

	LightDemo(3, 20);
	Serial.println("Ready");
}

uint8_t lightZ = 0;  //zone index
uint8_t lightM = 0;  //mode index

void loop() {
	ProcessSerial();


	if (millis() > nextMoveTime) {
		//Serial.println("Move Time Updated");
		nextMoveTime = millis() + 150;  //move every 50ms

		for (uint8_t i = 0; i < 10; i++) {
			//ProcessTentacle(i);
			MoveTentacle(i);
		}
	}
	/*
	if (millis() > nextBlinkTime) {
		nextBlinkTime = millis() + (BLINK_TIME );
		for (int i = 0; i < 5; i++) {
			for (int j = 0; j < 3; j++) {
				if (blinking[i][j]) {
					bool state = true;
					if (digitalRead(lights[i][j])) {
						state = false;
					}
					digitalWrite(lights[i][j], state);
				}
			}
		}
	}
	*/

	// running a for loop across multiple iterations of the main loop, running every blink_time/15 ms to give some variation in when the lights cycle
	if (millis() > nextBlinkTime) {
		nextBlinkTime = millis() + (BLINK_TIME / 15);  //blink every 500ms

		if (blinking[lightZ][lightM]) {
			// invert light state
			bool state = true;
			if (digitalRead(lights[lightZ][lightM])) {
				state = false;
			}
			digitalWrite(lights[lightZ][lightM], state);
		}
		// increment which mode (K -> T -> Z)
		lightM++;
		if (lightM >= 3) {
			lightM = 0;
			lightZ++;  // increment zone when all modes are blinked
		}
		if (lightZ >= 5) {
			lightZ = 0;  // reset to first zone after all zones are blinked
		}
	}
}

// Function Definitions
void ProcessSerial() {
	if (Serial.available() < MESSAGE_BYTES) {
		return;
	}

	// Debug recieved message
	Serial.print("Parsing serial: [");
	for (int i = 0; i < MESSAGE_BYTES; i++) {
		message[i] = Serial.read();
		Serial.print(message[i]);
		if (i != MESSAGE_BYTES - 1) {
			Serial.print(", ");
		}
	}
	Serial.println("]");

	// If there were more bytes sent than 4, clear the rest from the serial buffer
	while (Serial.available() > 0) {
		Serial.read();
	}

	if (message[0] == 'D') {
		Serial.println("Hell yeah");
		LightDemo(10, 60);
		return;
	}
	if (message[0] == 'S') {
		Serial.println("Sweeping");
		for (int i = 0; i < 10; i++) {
			Sweep(i);
		}
		delay(5000);
		//LightDemo(10, 60);
		return;
	}

	// Start parsing message
	if (message[0] == 't' || message[0] == 'T') {
		// Messages is a tentacle type
		bool mode = (message[3] == 'e' || message[3] == 'E');
		// true - tentacle enable
		// false - tentacle disable
		switch (message[1]) {
			case 'A':
			case 'a':
				// Tentacles in region A
				if (message[2] == '0') {
					// Target all tentacles in region A
					if (mode) {
						Serial.println("Enabling all tentacles in A");
						EnableTentacle(tA1);
						EnableTentacle(tA2);
						EnableTentacle(tA3);
					} else {
						Serial.println("Disabling all tentacles in A");
						DisableTentacle(tA1);
						DisableTentacle(tA2);
						DisableTentacle(tA3);
					}
				} else if (message[2] == '1') {
					// Target 1st tentacle in region A
					if (mode) {
						Serial.println("Enabling tentacle A1");
						EnableTentacle(tA1);
					} else {
						Serial.println("Disabling tentacle A1");
						DisableTentacle(tA1);
					}
				} else if (message[2] == '2') {
					// Target 2nd tentacle in region A
					if (mode) {
						Serial.println("Enabling tentacle A2");
						EnableTentacle(tA2);
					} else {
						Serial.println("Disabling tentacle A2");
						DisableTentacle(tA2);
					}
				} else if (message[2] == '3') {
					// Target 3rd tentacle in region A
					if (mode) {
						Serial.println("Enabling tentacle A3");
						EnableTentacle(tA3);
					} else {
						Serial.println("Disabling tentacle A3");
						DisableTentacle(tA3);
					}
				} else {
					Serial.print("Unable to enable / disable tentacle A");
					Serial.println(message[2]);
				}
				break;
			case 'D':
			case 'd':
				// Tentacles in region D
				if (message[2] == '0') {
					// Target all tentacles in region D
					if (mode) {
						Serial.println("Enabling all tentacles in D");
						EnableTentacle(tD1);
						EnableTentacle(tD2);
					} else {
						Serial.println("Disabling all tentacles in D");
						DisableTentacle(tD1);
						DisableTentacle(tD2);
					}
				} else if (message[2] == '1') {
					// Target 1st tentacle in region D
					if (mode) {
						Serial.println("Enabling tentacle D1");
						EnableTentacle(tD1);
					} else {
						Serial.println("Disabling tentacle D1");
						DisableTentacle(tD1);
					}
				} else if (message[2] == '2') {
					// Target 2nd rentacle in region D
					if (mode) {
						Serial.println("Enabling tentacle D2");
						EnableTentacle(tD2);
					} else {
						Serial.println("Disabling tentacle D2");
						DisableTentacle(tD2);
					}
				} else {
					Serial.print("Unable to enable / disable tentacle D");
					Serial.println(message[2]);
				}
				break;
			case 'N':
			case 'n':
				// Tentacles in region N
				if (message[2] == '0') {
					// Target all tentacles in region N
					if (mode) {
						Serial.println("Enabling all tentacles in N");
						EnableTentacle(tN1);
						EnableTentacle(tN2);
					} else {
						Serial.println("Disabling all tentacles in N");
						DisableTentacle(tN1);
						DisableTentacle(tN2);
					}
				} else if (message[2] == '1') {
					// Target 1st tentacle in region N
					if (mode) {
						Serial.println("Enabling tentacle N1");
						EnableTentacle(tN1);
					} else {
						Serial.println("Disabling tentacle N1");
						DisableTentacle(tN1);
					}
				} else if (message[2] == '2') {
					// Target 2nd tentacle in region N
					if (mode) {
						Serial.println("Enabling tentacle N2");
						EnableTentacle(tN2);
					} else {
						Serial.println("Disabling tentacle N2");
						DisableTentacle(tN2);
					}
				} else {
					Serial.print("Unable to enable / disable tentacle N");
					Serial.println(message[2]);
				}
				break;
			case 'W':
			case 'w':
				// Tentacles in region W
				if (message[2] == '0') {
					if (mode) {
						Serial.println("Enabling all tentacles in W");
						EnableTentacle(tW1);
					} else {
						Serial.println("Disabling all tentacles in W");
						DisableTentacle(tW1);
					}
				} else if (message[2] == '1') {
					if (mode) {
						Serial.println("Enabling tentacle W1");
						EnableTentacle(tW1);
					} else {
						Serial.println("Disabling tentacle W1");
						DisableTentacle(tW1);
					}
				} else {
					Serial.print("Unable to enable / disable tentacle W");
					Serial.println(message[2]);
				}
				break;
			case 'V':
			case 'v':
				// Tentacles in region V
				if (message[2] == '0') {
					// Target all tentacles in region V
					if (mode) {
						Serial.println("Enabling all tentacles in V");
						EnableTentacle(tV1);
						EnableTentacle(tV2);
					} else {
						Serial.println("Disabling all tentacles in V");
						DisableTentacle(tV1);
						DisableTentacle(tV2);
					}
				} else if (message[2] == '1') {
					// Target 1st tentacle in region V
					if (mode) {
						Serial.println("Enabling tentacle V1");
						EnableTentacle(tV1);
					} else {
						Serial.println("Disabling tentacle V1");
						DisableTentacle(tV1);
					}
				} else if (message[2] == '2') {
					// Target 2nd tentacle in region V
					if (mode) {
						Serial.println("Enabling tentacle V2");
						EnableTentacle(tV2);
					} else {
						Serial.println("Disabling tentacle V2");
						DisableTentacle(tV2);
					}
				} else {
					Serial.print("Unable to enable / disable tentacle V");
					Serial.println(message[2]);
				}
				break;
			default:
				Serial.println("Invalid Tentacle");
		}
	} else if (message[0] == 'l' || message[0] == 'L') {
		bool turnOn = (message[3] == 'b' || message[3] == 'B') || (message[3] == 'e' || message[3] == 'E');
		bool blink = (message[3] == 'b' || message[3] == 'B');

		switch (message[1]) {
			case 'A':
			case 'a':
				SetLight(ZA, message[2], turnOn);
				if (message[2] == 'k' || message[2] == 'K') {
					blinking[0][0] = blink;
				} else if (message[2] == 't' || message[2] == 'T') {
					blinking[0][1] = blink;
				} else if (message[2] == 'z' || message[2] == 'Z') {
					blinking[0][2] = blink;
				} else {
					Serial.println("Invalid Light");
				}
				break;
			case 'D':
			case 'd':
				SetLight(ZD, message[2], turnOn);
				if (message[2] == 'k' || message[2] == 'K') {
					blinking[1][0] = blink;
				} else if (message[2] == 't' || message[2] == 'T') {
					blinking[1][1] = blink;
				} else if (message[2] == 'z' || message[2] == 'Z') {
					blinking[1][2] = blink;
				} else {
					Serial.println("Invalid Light");
				}
				break;
			case 'N':
			case 'n':
				SetLight(ZN, message[2], turnOn);
				if (message[2] == 'k' || message[2] == 'K') {
					blinking[2][0] = blink;
				} else if (message[2] == 't' || message[2] == 'T') {
					blinking[2][1] = blink;
				} else if (message[2] == 'z' || message[2] == 'Z') {
					blinking[2][2] = blink;
				} else {
					Serial.println("Invalid Light");
				}
				break;
			case 'W':
			case 'w':
				SetLight(ZW, message[2], turnOn);
				if (message[2] == 'k' || message[2] == 'K') {
					blinking[3][0] = blink;
				} else if (message[2] == 't' || message[2] == 'T') {
					blinking[3][1] = blink;
				} else if (message[2] == 'z' || message[2] == 'Z') {
					blinking[3][2] = blink;
				} else {
					Serial.println("Invalid Light");
				}
				break;
			case 'V':
			case 'v':
				SetLight(ZV, message[2], turnOn);
				if (message[2] == 'k' || message[2] == 'K') {
					blinking[4][0] = blink;
				} else if (message[2] == 't' || message[2] == 'T') {
					blinking[4][1] = blink;
				} else if (message[2] == 'z' || message[2] == 'Z') {
					blinking[4][2] = blink;
				} else {
					Serial.println("Invalid Light");
				}
				break;
			default:
				Serial.println("Invalid Light Zone");
		}
	} else {
		Serial.println("Failed to parse");
		while (Serial.available()) { Serial.read(); }
	}
	return;
}

void InitLights(uint8_t iPins[]) {
	pinMode(iPins[0], OUTPUT);
	pinMode(iPins[1], OUTPUT);
	pinMode(iPins[2], OUTPUT);
}

void SetLight(uint8_t iPins[], char iType, bool iState) {
	switch (iType) {
		case 'K':
		case 'k':
			digitalWrite(iPins[0], iState);
			break;
		case 'Z':
		case 'z':
			digitalWrite(iPins[2], iState);
			break;
		case 'T':
		case 't':
			digitalWrite(iPins[1], iState);
			break;
		default:
			Serial.println("Invalid Light in Zone");
			break;
	}
}

void LightDemo(int times, int t) {
	for (int i = 0; i < times; i++) {
		SetLight(ZA, 'K', true);
		delay(t);
		SetLight(ZA, 'Z', true);
		delay(t);
		SetLight(ZA, 'T', true);
		delay(t);

		SetLight(ZD, 'K', true);
		delay(t);
		SetLight(ZD, 'Z', true);
		delay(t);
		SetLight(ZD, 'T', true);
		delay(t);

		SetLight(ZN, 'K', true);
		delay(t);
		SetLight(ZN, 'Z', true);
		delay(t);
		SetLight(ZN, 'T', true);
		delay(t);

		SetLight(ZV, 'K', true);
		delay(t);
		SetLight(ZV, 'Z', true);
		delay(t);
		SetLight(ZV, 'T', true);
		delay(t);

		SetLight(ZW, 'K', true);
		delay(t);
		SetLight(ZW, 'Z', true);
		delay(t);
		SetLight(ZW, 'T', true);
		delay(t);

		SetLight(ZA, 'K', false);
		delay(t);
		SetLight(ZA, 'Z', false);
		delay(t);
		SetLight(ZA, 'T', false);
		delay(t);

		SetLight(ZD, 'K', false);
		delay(t);
		SetLight(ZD, 'Z', false);
		delay(t);
		SetLight(ZD, 'T', false);
		delay(t);

		SetLight(ZN, 'K', false);
		delay(t);
		SetLight(ZN, 'Z', false);
		delay(t);
		SetLight(ZN, 'T', false);
		delay(t);

		SetLight(ZV, 'K', false);
		delay(t);
		SetLight(ZV, 'Z', false);
		delay(t);
		SetLight(ZV, 'T', false);
		delay(t);

		SetLight(ZW, 'K', false);
		delay(t);
		SetLight(ZW, 'Z', false);
		delay(t);
		SetLight(ZW, 'T', false);
		delay(t);
	}
}

void InitTentacle(uint8_t iTentacle) {

	// Configure Servo
	Tentacles[iTentacle].TentacleServo.attach(Tentacles[iTentacle].ServoPin);
	Tentacles[iTentacle].TentacleServo.write(Tentacles[iTentacle].RestAng);
}

void Sweep(uint8_t iTentacle) {

	Tentacles[iTentacle].TentacleServo.write(90);
	delay(500);
	Tentacles[iTentacle].TentacleServo.write(80);
	delay(500);
}

void EnableTentacle(uint8_t iTentacle) {
	//digitalWrite(Tentacles[iTentacle].ActivePin, HIGH);
	Tentacles[iTentacle].TentacleServo.write(Tentacles[iTentacle].RestAng);
	Tentacles[iTentacle].position = Tentacles[iTentacle].RestAng;
	Tentacles[iTentacle].Enabled = true;
	//Serial.print("Enabled tentacle: ");
	//Serial.println(iTentacle);
	//was bool as with more tentacles this had some cases where it would reject the enable. No longer used for feedback.
}

void DisableTentacle(uint8_t iTentacle) {
	//digitalWrite(Tentacles[iTentacle].ActivePin, LOW);
	Tentacles[iTentacle].TentacleServo.write(Tentacles[iTentacle].RestAng);
	Tentacles[iTentacle].position = Tentacles[iTentacle].RestAng;
	Tentacles[iTentacle].Enabled = false;
	//Serial.print("Disabled tentacle: ");
	//Serial.println(iTentacle);
}

void MoveTentacle(uint8_t iTentacle) {

	if (Tentacles[iTentacle].Enabled == false) {
		return;
	}
	uint8_t step = 2;
	if (Tentacles[iTentacle].direction == false) {
		step *= -1;
	}

	uint8_t new_pos = Tentacles[iTentacle].position + step;
	if (new_pos < Tentacles[iTentacle].MinAng) {
		new_pos = Tentacles[iTentacle].MinAng;
		Tentacles[iTentacle].direction = true;
	}
	if (new_pos > Tentacles[iTentacle].MaxAng) {
		new_pos = Tentacles[iTentacle].MaxAng;
		Tentacles[iTentacle].direction = false;
	}
	Tentacles[iTentacle].position = new_pos;

	//Serial.println(Tentacles[iTentacle].position);
	Tentacles[iTentacle].TentacleServo.write(Tentacles[iTentacle].position);
}

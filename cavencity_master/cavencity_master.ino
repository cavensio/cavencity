#include <RF24.h>
#include "slave_protocol.h"
#include "master_protocol.h"


// Radio
const uint8_t RADIO_ADDRESS[][6] = {"cave0", "cave1", "cave2"};
const uint8_t RADIO_CHANNEL = 69;
const uint8_t RADIO_CE_PIN = 9;
const uint8_t RADIO_CS_PIN = 10;
RF24 radio(RADIO_CE_PIN, RADIO_CS_PIN);

// Pins
const uint8_t CAVE1_USE_PIN = A0;
const uint8_t CAVE1_FAN_PIN = A1;
const uint8_t CAVE1_LED_PIN = 3;
const uint8_t CAVE2_USE_PIN = A4;
const uint8_t CAVE2_FAN_PIN = A5;
const uint8_t CAVE2_LED_PIN = 2;

// States
MasterSlaveActualState actualState;
MasterSlaveTargetState targetState;

// Setup
void setupRadio() {
  if (!radio.begin()) {
    Serial.println("Radio not ready");
    exit(0);
  }
  Serial.println("Setup radio");
  radio.setChannel(RADIO_CHANNEL);
  radio.setPALevel(RF24_PA_LOW); //RF24_PA_HIGH
  radio.setDataRate(RF24_2MBPS); //RF24_250KBPS
  radio.enableDynamicPayloads();
  radio.enableAckPayload();
  radio.openReadingPipe(1, RADIO_ADDRESS[0]);
  radio.stopListening();
}

void setupControls() {
  pinMode(CAVE1_USE_PIN, INPUT_PULLUP);
  pinMode(CAVE1_FAN_PIN, INPUT_PULLUP);
  pinMode(CAVE1_LED_PIN, OUTPUT);

  pinMode(CAVE2_USE_PIN, INPUT_PULLUP);
  pinMode(CAVE2_FAN_PIN, INPUT_PULLUP);
  pinMode(CAVE2_LED_PIN, OUTPUT);
}

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("cavencity_master");
  setupControls();
  setupRadio();
}

void setSlaveState(uint8_t slaveIndex) {
  radio.stopListening();
  radio.openWritingPipe(RADIO_ADDRESS[slaveIndex + 1]);
  delay(1);
  
  SlaveTargetState &slaveTargetState = targetState.slaveStates[slaveIndex];
  SlaveActualState &slaveActualState = actualState.slaveStates[slaveIndex];
  NetStat &slaveNetStat = actualState.slaveStats[slaveIndex];

  uint32_t start_timer = micros();
  uint8_t report = radio.write(&slaveTargetState, sizeof(slaveTargetState));
  uint32_t end_timer = micros();
  uint32_t time = end_timer - start_timer;

  if (report) {
    slaveNetStat.latency = time;
    uint8_t pipe;
    if (radio.available(&pipe)) {
      slaveNetStat.online = 1;
      Serial.print(" Request ok: lat=");
      Serial.print(time);

      radio.read(&slaveActualState, sizeof(slaveActualState));
      Serial.print(" Response: size=");
      Serial.print(radio.getDynamicPayloadSize());
      Serial.print(", pipe=");
      Serial.print(pipe);
      Serial.print(", data=");
      Serial.print(slaveActualState.uptime);
      Serial.print(" ");
      Serial.print(slaveActualState.counter);
      Serial.print(" ");
      Serial.print(slaveActualState.fanLevel);
      Serial.print(" ");
      Serial.print(slaveActualState.lightLevel);
      Serial.print(" ");
      Serial.println(slaveActualState.damperClosed);
    } else {
      Serial.print(" Response fail: lat=");
      Serial.println(time);
      slaveNetStat.online = 0;
      slaveNetStat.errors++;
    }
  } else {
    Serial.print(" Request fail: time=");
    Serial.println(time);
    slaveNetStat.online = 0;
    slaveNetStat.errors++;
  }
}


void updateMasterVariables() {
  actualState.masterState.uptime = millis() / 1000;
  actualState.masterState.counter++;
}

void readCommand() {
  if (Serial.available()) {
    int command = Serial.read();
    switch (command) {
      case 'P':
        updateMasterVariables();
        serialPrintActualState(actualState);
        break;
      case 'S':
        updateMasterVariables();
        serialParseTargetState(targetState);
        setSlaveState(0);
        setSlaveState(1);
        serialPrintActualState(actualState);
        break;
      case ' ':
      case '\n':
      case '\xff':
        break;
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
    }
  }
}

void loop() {
  readCommand();

  if (actualState.slaveStats[0].online) {
    if (actualState.slaveStates[0].fanLevel == 0) {
      digitalWrite(CAVE1_LED_PIN, HIGH);
    } else {
      digitalWrite(CAVE1_LED_PIN, LOW);
      delay(250);
      digitalWrite(CAVE1_LED_PIN, HIGH);
    }
  } else {
    digitalWrite(CAVE1_LED_PIN, LOW);
  }
  
  if (actualState.slaveStats[1].online) {
    if (actualState.slaveStates[1].fanLevel == 0) {
      digitalWrite(CAVE2_LED_PIN, HIGH);
    } else {
      digitalWrite(CAVE2_LED_PIN, LOW);
      delay(250);
      digitalWrite(CAVE2_LED_PIN, HIGH);
    }
  } else {
    digitalWrite(CAVE2_LED_PIN, LOW);
  }
}

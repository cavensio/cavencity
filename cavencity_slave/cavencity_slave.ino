#include <RF24.h>
#include "slave_protocol.h"
#include "tick_trick.h"

// Radio
const uint8_t RADIO_ADDRESS[][6] = {"cave0", "cave1", "cave2"};
const uint8_t RADIO_CHANNEL = 69;
const uint8_t RADIO_CE_PIN = 9;
const uint8_t RADIO_CS_PIN = 10;
const RF24 radio(RADIO_CE_PIN, RADIO_CS_PIN);

// Pins
const uint8_t FAN_LED_PIN = 3;
const uint8_t LIGHT_LED_PIN = 5;
const uint8_t MASTER_OFFLINE_LED_PIN = 2;
const uint8_t SLAVE_SELECT_PIN = A0;
uint8_t slave_number = 1;

// States
const uint16_t SIGNAL_FROM_MASTER_TIMEOUT = 5000;
const uint16_t ACK_PREPARE_INTERVAL = 100;

uint8_t masterOnline = 1;
uint32_t lastOnlineMillis = 0;

SlaveTargetState targetState;
SlaveActualState actualState;

TickTrick fanChanger(2000);
TickTrick lightChanger(50);

const uint8_t FAN_LEVEL_MAX = 5;
const uint8_t LIGHT_LEVEL_MAX = 100;

void setupRadio() {
  if (!radio.begin()) {
    exit(0);
  }
  radio.setChannel(RADIO_CHANNEL);
  radio.setPALevel(RF24_PA_LOW); //RF24_PA_HIGH
  radio.setDataRate(RF24_2MBPS); //RF24_250KBPS
  radio.enableDynamicPayloads();
  radio.enableAckPayload();
  radio.openWritingPipe(RADIO_ADDRESS[0]);
  radio.openReadingPipe(1, RADIO_ADDRESS[slave_number]);
  prepareAck();
  radio.startListening();
}

void setupControls() {
  pinMode(FAN_LED_PIN, OUTPUT);
  pinMode(LIGHT_LED_PIN, OUTPUT);
  pinMode(MASTER_OFFLINE_LED_PIN, OUTPUT);
  pinMode(SLAVE_SELECT_PIN, INPUT_PULLUP);
  slave_number = digitalRead(SLAVE_SELECT_PIN) ? 1 : 2;
}

void setup() {
  setupControls();
  setupRadio();
}

void flagMasterOnline() {
  actualState.counter++;
  lastOnlineMillis = millis();
  if (!masterOnline) {
    masterOnline = true;
    digitalWrite(MASTER_OFFLINE_LED_PIN, LOW);
  }
}

void flagMasterOffline() {
  if (masterOnline) {
    masterOnline = false;
    digitalWrite(MASTER_OFFLINE_LED_PIN, HIGH);
  }
}

void calcState() {
  actualState.fanLevel = fanChanger.tick(actualState.fanLevel, targetState.fanLevel);
  analogWrite(FAN_LED_PIN, map(actualState.fanLevel, 0, FAN_LEVEL_MAX, 0, 255));

  actualState.lightLevel = lightChanger.tick(actualState.lightLevel, targetState.lightLevel);
  analogWrite(LIGHT_LED_PIN, map(actualState.lightLevel, 0, LIGHT_LEVEL_MAX, 0, 255));
}

void prepareAck() {
  actualState.uptime = millis() / 1000;
  radio.flush_tx();
  radio.writeAckPayload(1, &actualState, sizeof(actualState));
}

void loop() {
  if (radio.available()) {
    radio.read(&targetState, sizeof(targetState));
    flagMasterOnline();
    prepareAck();
  } else {
    uint32_t now = millis();
    if (now - lastOnlineMillis > ACK_PREPARE_INTERVAL) {
      prepareAck();
    }

    if (now - lastOnlineMillis > SIGNAL_FROM_MASTER_TIMEOUT) {
      // indicate master as offline after 5 seconds of radio inactivity
      flagMasterOffline();
    }
  }
  calcState();
}

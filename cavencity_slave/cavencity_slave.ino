#include <RF24.h>

struct MasterRequest {
  uint8_t fan;
};

struct SlaveResponse {
  uint8_t fan;
  uint8_t counter;
  uint32_t millis;
};

const uint8_t CAVE_ADDRESS[][6] = {"cave0", "cave1", "cave2"};

const uint8_t RADIO_CHANNEL = 69;
const uint8_t RADIO_SPEED = RF24_2MBPS; //RF24_250KBPS
const uint8_t RADIO_POWER = RF24_PA_LOW; //RF24_PA_HIGH

const uint8_t RADIO_CE_PIN = 9;
const uint8_t RADIO_CS_PIN = 10;

SlaveResponse response;

RF24 radio(RADIO_CE_PIN, RADIO_CS_PIN);

const uint8_t FAN_LED_PIN = 3;
const uint8_t OFFLINE_LED_PIN = 2;
const uint8_t SLAVE_SELECT_PIN = A0;

uint8_t slave_number = 1;

void setupRadio() {
  if (!radio.begin()) {
    exit(0);
  }
  radio.setChannel(RADIO_CHANNEL);
  radio.setPALevel(RADIO_POWER);
  radio.setDataRate(RADIO_SPEED);
  radio.enableDynamicPayloads();
  radio.enableAckPayload();
  radio.openWritingPipe(CAVE_ADDRESS[0]);
  radio.openReadingPipe(1, CAVE_ADDRESS[slave_number]);
  radio.writeAckPayload(1, &response, sizeof(response));
  radio.startListening();
}

void setupControls() {
  pinMode(FAN_LED_PIN, OUTPUT);
  pinMode(OFFLINE_LED_PIN, OUTPUT);
  pinMode(SLAVE_SELECT_PIN, INPUT_PULLUP);
  slave_number = digitalRead(SLAVE_SELECT_PIN) ? 1 : 2;
}

void setup() {
  setupControls();
  setupRadio();
}

void setOfflineState(uint8_t state) {
  if (state) {
    digitalWrite(OFFLINE_LED_PIN, HIGH);
  } else {
    digitalWrite(OFFLINE_LED_PIN, LOW);
  }
}

void setFanState(uint8_t state) {
  if (state) {
    digitalWrite(FAN_LED_PIN, HIGH);
  } else {
    digitalWrite(FAN_LED_PIN, LOW);
  }
}

void loop() {
  if (radio.available()) {
    MasterRequest request;
    radio.read(&request, sizeof(request));
    response.fan = request.fan;
    response.counter++;
    response.millis = millis();
    radio.writeAckPayload(1, &response, sizeof(response));

    setOfflineState(0);
    setFanState(response.fan);
  } else {
    if (millis() - response.millis > 5000) {
      setOfflineState(1);
    }
  }
}

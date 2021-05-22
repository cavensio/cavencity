#include <RF24.h>

// Common structures
struct MasterRequest {
  uint8_t fan;
};

struct SlaveResponse {
  uint8_t fan;
  uint8_t counter;
  uint32_t millis;
};

const uint8_t CONNECTION_ERROR = 255;

// Radio
const uint8_t CAVE_ADDRESS[][6] = {"cave0", "cave1", "cave2"};

const uint8_t CHANNEL = 69;
const uint8_t RADIO_SPEED = RF24_2MBPS; //RF24_250KBPS
const uint8_t RADIO_POWER = RF24_PA_LOW; //RF24_PA_HIGH
const uint8_t RADIO_CE_PIN = 9;
const uint8_t RADIO_CS_PIN = 10;

RF24 radio(RADIO_CE_PIN, RADIO_CS_PIN);

// Controls
const uint8_t CAVE1_USE_PIN = A0;
const uint8_t CAVE1_FAN_PIN = A1;
const uint8_t CAVE1_LED_PIN = 3;

const uint8_t CAVE2_USE_PIN = A4;
const uint8_t CAVE2_FAN_PIN = A5;
const uint8_t CAVE2_LED_PIN = 2;

// Setup
void setupRadio() {
  if (!radio.begin()) {
    Serial.println("Radio not ready");
    exit(0);
  }
  Serial.println("Setup radio");
  radio.setChannel(CHANNEL);
  radio.setPALevel(RADIO_POWER);
  radio.setDataRate(RADIO_SPEED);
  radio.enableDynamicPayloads();
  radio.enableAckPayload();
  radio.openReadingPipe(1, CAVE_ADDRESS[0]);
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

SlaveResponse sendCommand(uint8_t caveNumber, MasterRequest request) {
  SlaveResponse response;
  Serial.print("Fan: ");
  Serial.print(request.fan);

  radio.openWritingPipe(CAVE_ADDRESS[caveNumber]);

  uint32_t start_timer = micros();
  uint8_t report = radio.write(&request, sizeof(request));
  uint32_t end_timer = micros();
  uint32_t time1 = end_timer - start_timer;

  if (report) {
    Serial.print(" Request ok: time=");
    Serial.print(time1);
    uint8_t pipe;
    if (radio.available(&pipe)) {
      radio.read(&response, sizeof(response));
      Serial.print(" Response: bytes=");
      Serial.print(radio.getDynamicPayloadSize());
      Serial.print(", pipe=");
      Serial.print(pipe);
      Serial.print(", data=");
      Serial.print(response.fan);
      Serial.print(" ");
      Serial.print(response.counter);
      Serial.print(" ");
      Serial.println(response.millis);
    } else {
      Serial.println(" Response fail");
      response.fan = CONNECTION_ERROR;
    }
  } else {
    Serial.print(" Request fail: time=");
    Serial.println(time1);
    response.fan = CONNECTION_ERROR;
  }
  return response;
}


void loop() {
  //  if (Serial.available() > 0) {
  //    request.command = Serial.parseInt();
  //    Serial.print("Command: ");
  //    Serial.println(request.command);
  //  }

  uint8_t cave1_use = !digitalRead(CAVE1_USE_PIN);
  if (cave1_use) {
    uint8_t cave1_fan = !digitalRead(CAVE1_FAN_PIN);
    MasterRequest request = {cave1_fan};
    SlaveResponse response = sendCommand(1, request);

    if (response.fan == 0) {
      digitalWrite(CAVE1_LED_PIN, HIGH);
    } else if (response.fan == 1) {
      digitalWrite(CAVE1_LED_PIN, LOW);
      delay(333);
      digitalWrite(CAVE1_LED_PIN, HIGH);
    }   else if (response.fan == CONNECTION_ERROR) {
      digitalWrite(CAVE1_LED_PIN, LOW);
    }
  } else {
    digitalWrite(CAVE1_LED_PIN, LOW);
  }


  uint8_t cave2_use = !digitalRead(CAVE2_USE_PIN);
  if (cave2_use) {
    uint8_t cave2_fan = !digitalRead(CAVE2_FAN_PIN);
    MasterRequest request = {cave2_fan};
    SlaveResponse response = sendCommand(2, request);

    if (response.fan == 0) {
      digitalWrite(CAVE2_LED_PIN, HIGH);
    } else if (response.fan == 1) {
      digitalWrite(CAVE2_LED_PIN, LOW);
      delay(333);
      digitalWrite(CAVE2_LED_PIN, HIGH);
    }   else if (response.fan == CONNECTION_ERROR) {
      digitalWrite(CAVE2_LED_PIN, LOW);
    }
  } else {
    digitalWrite(CAVE2_LED_PIN, LOW);
  }

  delay(1000);
}

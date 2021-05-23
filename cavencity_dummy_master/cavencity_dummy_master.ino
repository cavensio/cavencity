/**
   Dummy master emulates cavencity serial protocol for dev and debug purposes.
   It can be uploaded to a bare Arduino without any pins or modules connected.
   
   Serial commands:
   - C - switch to continuous mode and print state every second
   - P <state string> - push state
   - R - read state
   - S - switch continuous mode off
   - T <time> - sleep for a given amount of millis to simulate timeouts
*/

const char MASTER_UPTIME[] = "mu";
const char MASTER_COUNTER[] = "mc";
const char MASTER_BACKLIGHT[] = "mb";
const char SLAVE1_ONLINE[] = "s1o";
const char SLAVE1_UPTIME[] = "s1u";
const char SLAVE1_COUNTER[] = "s1c";
const char SLAVE1_FAN[] = "s1f";
const char SLAVE1_DAMPER[] = "s1d";
const char SLAVE1_LIGHT[] = "s1l";
const char SLAVE2_ONLINE[] = "s2o";
const char SLAVE2_UPTIME[] = "s2u";
const char SLAVE2_COUNTER[] = "s2c";
const char SLAVE2_FAN[] = "s2f";
const char SLAVE2_DAMPER[] = "s2d";
const char SLAVE2_LIGHT[] = "s2l";

uint32_t masterUptime = 0;
uint32_t masterCounter = 0;
uint8_t masterBacklight = 0;
uint8_t slave1Online = 0;
uint32_t slave1Uptime = 0;
uint32_t slave1Counter = 0;
uint8_t slave1Fan = 0;
uint8_t slave1Damper = 0;
uint8_t slave1Light = 0;
uint8_t slave2Online = 0;
uint32_t slave2Uptime = 0;
uint32_t slave2Counter = 0;
uint8_t slave2Fan = 0;
uint8_t slave2Damper = 0;
uint8_t slave2Light = 0;

bool continuousMode = false;

void setup() {
  Serial.setTimeout(1000);
  Serial.begin(115200);
  while (!Serial);
  Serial.println("cavencity_dummy_master");
}

void printDataItem(char* key, uint32_t value) {
  Serial.print(key);
  Serial.print('=');
  Serial.print(value);
  Serial.print(' ');
}

void printState() {
  setVariables();
  Serial.print('\x1e');
  printDataItem(MASTER_UPTIME, masterUptime);
  printDataItem(MASTER_COUNTER, masterCounter);
  printDataItem(MASTER_BACKLIGHT, masterBacklight);
  printDataItem(SLAVE1_ONLINE, slave1Online);
  printDataItem(SLAVE1_UPTIME, slave1Uptime);
  printDataItem(SLAVE1_COUNTER, slave1Counter);
  printDataItem(SLAVE1_FAN, slave1Fan);
  printDataItem(SLAVE1_DAMPER, slave1Damper);
  printDataItem(SLAVE1_LIGHT, slave1Light);
  printDataItem(SLAVE2_ONLINE, slave2Online);
  printDataItem(SLAVE2_UPTIME, slave2Uptime);
  printDataItem(SLAVE2_COUNTER, slave2Counter);
  printDataItem(SLAVE2_FAN, slave2Fan);
  printDataItem(SLAVE2_DAMPER, slave2Damper);
  printDataItem(SLAVE2_LIGHT, slave2Light);
  Serial.println();
}

void setVariables() {
  masterUptime = millis();
  slave1Uptime = masterUptime + 1111;
  slave2Uptime = masterUptime + 2222;

  masterCounter += 1;
  slave1Counter = masterCounter + 101;
  slave2Counter = masterCounter + 202;

  slave1Online = 1;
  slave2Online = 1;
}

void readPushState() {
  while (true) {
    int next = Serial.peek();
    if (next == -1) {
      continue;
    }
    if (next == '\n') {
      break;
    }

    String key = Serial.readStringUntil('=');
    key.trim();
    if (!key) {
      break;
    }
    int val = Serial.parseInt(SKIP_WHITESPACE);

    Serial.print(key);
    Serial.print('=');
    Serial.print(val);

    if (val > 255) {
      Serial.println(" Invalid value");
      continue;
    }
    if (key == MASTER_BACKLIGHT) {
      masterBacklight = val;
    } else if (key == SLAVE1_FAN) {
      slave1Fan = val;
    } else if (key == SLAVE2_FAN) {
      slave2Fan = val;
    } else if (key == SLAVE1_DAMPER) {
      slave1Damper = val;
    } else if (key == SLAVE2_DAMPER) {
      slave2Damper = val;
    } else if (key == SLAVE1_LIGHT) {
      slave1Light = val;
    } else if (key == SLAVE2_LIGHT) {
      slave2Light = val;
    } else {
      Serial.println(" Unknown key");
      continue;
    }
    Serial.println();
  }
}

void readCommand() {
  if (Serial.available()) {
    int command = Serial.read();
    switch (command) {
      case 'C':
        continuousMode = true;
        break;
      case 'P':
        readPushState();
        break;
      case 'R':
        printState();
        break;
      case 'S':
        continuousMode = false;
        break;
      case 'T':
        int timeout = Serial.parseInt();
        delay(timeout);
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

void waitForSerialOrTimeout(uint32_t timeoutMillis) {
  for (uint32_t i = 0; i < timeoutMillis && !Serial.available(); i++) {
    delay(1);
  }
}

void loop() {
  readCommand();

  if (continuousMode) {
    printState();
    waitForSerialOrTimeout(1000);
  }
}

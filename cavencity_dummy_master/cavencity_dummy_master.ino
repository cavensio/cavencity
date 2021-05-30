/**
   Dummy master emulates cavencity serial protocol for dev and debug purposes.
   It can be uploaded to a bare Arduino without any pins or modules connected.

   Serial commands:
   - C - switch to continuous mode and print state every second
   - X - switch continuous mode off
   - S <state string> - set state
   - P - print state string
   - T <time> - sleep for a given amount of millis to simulate timeout
*/

const char MASTER_UPTIME[] = "mu";
const char MASTER_COUNTER[] = "mc";
const char MASTER_BACKLIGHT[] = "mb";

const char SLAVE1_ONLINE[] = "s1o";
const char SLAVE1_UPTIME[] = "s1u";
const char SLAVE1_COUNTER[] = "s1c";

const char SLAVE1_FAN[] = "s1fl";
const char SLAVE1_LIGHT[] = "s1ll";
const char SLAVE1_DAMPER[] = "s1d";

const char SLAVE2_ONLINE[] = "s2o";
const char SLAVE2_UPTIME[] = "s2u";
const char SLAVE2_COUNTER[] = "s2c";

const char SLAVE2_FAN[] = "s2fl";
const char SLAVE2_LIGHT[] = "s2ll";
const char SLAVE2_DAMPER[] = "s2d";



uint32_t masterUptime = 0;
uint32_t masterCounter = 0;
uint8_t slave1Online = 0;
uint32_t slave1Uptime = 0;
uint32_t slave1Counter = 0;
uint8_t slave2Online = 0;
uint32_t slave2Uptime = 0;
uint32_t slave2Counter = 0;

// Target values
uint8_t masterBacklight = 0;
uint8_t slave1Fan = 0;
uint8_t slave1Damper = 0;
uint8_t slave1Light = 0;
uint8_t slave2Fan = 0;
uint8_t slave2Damper = 0;
uint8_t slave2Light = 0;

// Actual values
uint8_t masterBacklightActual = 0;
uint8_t slave1FanActual = 0;
uint8_t slave1DamperActual = 0;
uint8_t slave1LightActual = 0;
uint8_t slave2FanActual = 0;
uint8_t slave2DamperActual = 0;
uint8_t slave2LightActual = 0;


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
  printDataItem(MASTER_BACKLIGHT, masterBacklightActual);
  printDataItem(SLAVE1_ONLINE, slave1Online);
  printDataItem(SLAVE1_UPTIME, slave1Uptime);
  printDataItem(SLAVE1_COUNTER, slave1Counter);
  printDataItem(SLAVE1_FAN, slave1FanActual);
  printDataItem(SLAVE1_DAMPER, slave1DamperActual);
  printDataItem(SLAVE1_LIGHT, slave1LightActual);
  printDataItem(SLAVE2_ONLINE, slave2Online);
  printDataItem(SLAVE2_UPTIME, slave2Uptime);
  printDataItem(SLAVE2_COUNTER, slave2Counter);
  printDataItem(SLAVE2_FAN, slave2FanActual);
  printDataItem(SLAVE2_DAMPER, slave2DamperActual);
  printDataItem(SLAVE2_LIGHT, slave2LightActual);
  Serial.println();
}

uint8_t justifyVariable(uint8_t targetValue, uint8_t actualValue) {
  if (targetValue > actualValue) {
    return ++actualValue;
  } else if (targetValue < actualValue) {
    return --actualValue;
  } else {
    return actualValue;
  }
}

void setVariables() {
  masterUptime = millis();

  masterCounter += 1;
  masterBacklightActual = justifyVariable(masterBacklight, masterBacklightActual);

  if (masterCounter % 15 > 0 && masterCounter % 15 < 10) {
    slave1Online = 1;
    slave1Counter++;
    slave1Uptime = masterUptime + 1234;
    slave1FanActual = justifyVariable(slave1Fan, slave1FanActual);
    slave1DamperActual = justifyVariable(slave1Damper, slave1DamperActual);
    slave1LightActual = justifyVariable(slave1Light, slave1LightActual);
  } else {
    slave1Online = 0;
  }

  if (masterCounter % 25 > 3 && masterCounter % 25 < 17 ) {
    slave2Online = 1;
    slave2Counter++;
    slave2Uptime = masterUptime + 56789;
    slave2FanActual = justifyVariable(slave2Fan, slave2FanActual);
    slave2DamperActual = justifyVariable(slave2Damper, slave2DamperActual);
    slave2LightActual = justifyVariable(slave2Light, slave2LightActual);
  } else {
    slave2Online = 0;
  }
}

void setState() {
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

//    Serial.print(key);
//    Serial.print('=');
//    Serial.print(val);

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
//    Serial.println();
  }
}

void readCommand() {
  if (Serial.available()) {
    int command = Serial.read();
    switch (command) {
      case 'C':
        continuousMode = true;
        break;
      case 'X':
        continuousMode = false;
        break;
      case 'P':
        printState();
        break;
      case 'S':
        setState();
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

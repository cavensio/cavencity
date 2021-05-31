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
#include "slave_protocol.h"
#include "master_protocol.h"

// States
MasterSlaveActualState actualState;
MasterSlaveTargetState targetState;

bool continuousMode = false;

void setup() {
  Serial.setTimeout(1000);
  Serial.begin(115200);
  while (!Serial);
  Serial.println("cavencity_dummy_master");
}

uint8_t justifyVariable(uint8_t targetValue, uint8_t actualValue, uint8_t step = 1) {
  int8_t diff = targetValue - actualValue;
  if (diff > 0) {
    return actualValue += min(diff, step);
  } else if (diff < 0) {
    return actualValue -= min(-diff, step);
  } else {
    return actualValue;
  }
}

void calcVariables() {
  actualState.masterState.uptime = millis() / 1000;
  actualState.masterState.counter++;
  actualState.masterState.backlight = justifyVariable(targetState.masterState.backlight, actualState.masterState.backlight);

  if (actualState.masterState.counter % 15 > 0 && actualState.masterState.counter % 15 < 10) {
    actualState.slaveStats[0].online = 1;
    actualState.slaveStats[0].latency = random(500, 1500);

    actualState.slaveStates[0].counter++;
    actualState.slaveStates[0].uptime = actualState.masterState.uptime + 1234;

    actualState.slaveStates[0].fanLevel = justifyVariable(targetState.slaveStates[0].fanLevel,
                                          actualState.slaveStates[0].fanLevel);
    actualState.slaveStates[0].lightLevel = justifyVariable(targetState.slaveStates[0].lightLevel,
                                            actualState.slaveStates[0].lightLevel, 5);
    actualState.slaveStates[0].damperClosed = justifyVariable(targetState.slaveStates[0].damperClosed,
        actualState.slaveStates[0].damperClosed);
  } else {
    actualState.slaveStats[0].online = 0;
  }

  if (actualState.masterState.counter % 25 > 3 && actualState.masterState.counter % 25 < 17 ) {
    actualState.slaveStats[1].online = 1;
    actualState.slaveStats[1].latency = random(500, 1500);

    actualState.slaveStates[1].counter++;
    actualState.slaveStates[1].uptime = actualState.masterState.uptime + 56789;

    actualState.slaveStates[1].fanLevel = justifyVariable(targetState.slaveStates[1].fanLevel,
                                          actualState.slaveStates[1].fanLevel);
    actualState.slaveStates[1].lightLevel = justifyVariable(targetState.slaveStates[1].lightLevel,
                                            actualState.slaveStates[1].lightLevel, 5);
    actualState.slaveStates[1].damperClosed = justifyVariable(targetState.slaveStates[1].damperClosed,
        actualState.slaveStates[1].damperClosed);
  } else {
    actualState.slaveStats[1].online = 0;
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
        calcVariables();
        serialPrintActualState(actualState);
        break;
      case 'S':
        serialParseTargetState(targetState);
        calcVariables();
        serialPrintActualState(actualState);
        break;
      case 'T':
        delay(Serial.parseInt());
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
    calcVariables();
    serialPrintActualState(actualState);
    waitForSerialOrTimeout(1000);
  }
}

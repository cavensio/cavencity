#ifndef CAVE_MASTER_PROTOCOL
#define CAVE_MASTER_PROTOCOL

#include "slave_protocol.h"

const char MASTER_UPTIME_TAG[] = "mu";
const char MASTER_COUNTER_TAG[] = "mc";
const char MASTER_BACKLIGHT_TAG[] = "mbl";

const char SLAVE1_ONLINE_TAG[] = "s1o";
const char SLAVE1_UPTIME_TAG[] = "s1u";
const char SLAVE1_COUNTER_TAG[] = "s1c";
const char SLAVE1_LATENCY_TAG[] = "s1l";
const char SLAVE1_ERRORS_TAG[] = "s1e";
const char SLAVE1_FAN_LEVEL_TAG[] = "s1fl";
const char SLAVE1_LIGHT_LEVEL_TAG[] = "s1ll";
const char SLAVE1_DAMPER_CLOSED_TAG[] = "s1dc";

const char SLAVE2_ONLINE_TAG[] = "s2o";
const char SLAVE2_UPTIME_TAG[] = "s2u";
const char SLAVE2_COUNTER_TAG[] = "s2c";
const char SLAVE2_LATENCY_TAG[] = "s2l";
const char SLAVE2_ERRORS_TAG[] = "s2e";
const char SLAVE2_FAN_LEVEL_TAG[] = "s2fl";
const char SLAVE2_LIGHT_LEVEL_TAG[] = "s2ll";
const char SLAVE2_DAMPER_CLOSED_TAG[] = "s2dc";

struct MasterTargetState {
  uint8_t backlight;
};

struct MasterSlaveTargetState {
  MasterTargetState masterState;
  SlaveTargetState slaveStates[2];
};

struct MasterActualState {
  uint32_t counter;
  uint32_t uptime;
  uint8_t backlight;
};

struct NetStat {
  uint8_t online;
  uint32_t latency;
  uint32_t errors;
};

struct MasterSlaveActualState {
  MasterActualState masterState;
  SlaveActualState slaveStates[2];
  NetStat slaveStats[2];
};

void printKeyValue(const char* key, uint32_t value) {
  Serial.print(key);
  Serial.print('=');
  Serial.print(value);
  Serial.print(' ');
}

void serialPrintActualState(MasterSlaveActualState const &state) {
  Serial.print('\x1e');
  printKeyValue(MASTER_UPTIME_TAG, state.masterState.uptime);
  printKeyValue(MASTER_COUNTER_TAG, state.masterState.counter);
  printKeyValue(MASTER_BACKLIGHT_TAG, state.masterState.backlight);

  printKeyValue(SLAVE1_ONLINE_TAG, state.slaveStats[0].online);
  printKeyValue(SLAVE1_LATENCY_TAG, state.slaveStats[0].latency);
  printKeyValue(SLAVE1_ERRORS_TAG, state.slaveStats[0].errors);
  
  printKeyValue(SLAVE1_UPTIME_TAG, state.slaveStates[0].uptime);
  printKeyValue(SLAVE1_COUNTER_TAG, state.slaveStates[0].counter);
  printKeyValue(SLAVE1_FAN_LEVEL_TAG, state.slaveStates[0].fanLevel);
  printKeyValue(SLAVE1_LIGHT_LEVEL_TAG, state.slaveStates[0].lightLevel);
  printKeyValue(SLAVE1_DAMPER_CLOSED_TAG, state.slaveStates[0].damperClosed);

  printKeyValue(SLAVE2_ONLINE_TAG, state.slaveStats[1].online);
  printKeyValue(SLAVE2_LATENCY_TAG, state.slaveStats[1].latency);
  printKeyValue(SLAVE2_ERRORS_TAG, state.slaveStats[1].errors);
  printKeyValue(SLAVE2_UPTIME_TAG, state.slaveStates[1].uptime);
  printKeyValue(SLAVE2_COUNTER_TAG, state.slaveStates[1].counter);
  printKeyValue(SLAVE2_FAN_LEVEL_TAG, state.slaveStates[1].fanLevel);
  printKeyValue(SLAVE2_LIGHT_LEVEL_TAG, state.slaveStates[1].lightLevel);
  printKeyValue(SLAVE2_DAMPER_CLOSED_TAG, state.slaveStates[1].damperClosed);

  Serial.println();
}

void serialParseTargetState(MasterSlaveTargetState &state) {

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

    if (key == MASTER_BACKLIGHT_TAG) {
      state.masterState.backlight = val;
    } else if (key == SLAVE1_FAN_LEVEL_TAG) {
      state.slaveStates[0].fanLevel = val;
    } else if (key == SLAVE2_FAN_LEVEL_TAG) {
      state.slaveStates[1].fanLevel = val;
    } else if (key == SLAVE1_LIGHT_LEVEL_TAG) {
      state.slaveStates[0].lightLevel = val;
    } else if (key == SLAVE2_LIGHT_LEVEL_TAG) {
      state.slaveStates[1].lightLevel = val;
    } else if (key == SLAVE1_DAMPER_CLOSED_TAG) {
      state.slaveStates[0].damperClosed = val;
    } else if (key == SLAVE2_DAMPER_CLOSED_TAG) {
      state.slaveStates[1].damperClosed  = val;
    } else {
      Serial.println(" Unknown key");
      continue;
    }
    Serial.println();
  }
}

#endif

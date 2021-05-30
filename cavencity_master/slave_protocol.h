#ifndef CAVE_SLAVE_PROTOCOL
#define CAVE_SLAVE_PROTOCOL

struct SlaveTargetState {
  uint8_t fanLevel;
  uint8_t lightLevel;
  uint8_t damperClosed;
};

struct SlaveActualState {
  uint32_t counter;
  uint32_t uptime;
  uint8_t fanLevel;
  uint8_t lightLevel;
  uint8_t damperClosed;
};

#endif

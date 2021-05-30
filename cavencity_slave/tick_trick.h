/**
   Long-running discrete process without using of delay functions.
*/
#ifndef CAVE_TICK_TRICK
#define CAVE_TICK_TRICK

class TickTrick {
  private:
    uint32_t lastChangeTimestamp = 0;
    uint32_t changeRate = 0;
  public:
    // changeRate = Time in millis to increment/decrement the value
    TickTrick(uint8_t changeRate): changeRate(changeRate) {}

    uint32_t tick(uint32_t actualValue, uint32_t targetValue) {
      if (actualValue != targetValue) {
        uint32_t now = millis();
        if (now - lastChangeTimestamp > changeRate) {
          lastChangeTimestamp = now;
          int32_t diff = actualValue - targetValue;
          if (diff > 0) {
            actualValue--;
          }  else if (diff < 0) {
            actualValue++;
          }
        }
      }
      return actualValue;
    }
};

#endif

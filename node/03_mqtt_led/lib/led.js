import gpio from "rpi-gpio";

const LED_PIN = 40;

const led = class {
  constructor() {
    // LED ピンをOUT方向に設定
    gpio.setup(LED_PIN, gpio.DIR_OUT, function () {
      // LED ピンをhighに設定
      gpio.write(LED_PIN, true);
    });
  }

  on(callback) {
    gpio.write(LED_PIN, false, callback);
  }

  off(callback) {
    gpio.write(LED_PIN, true, callback);
  }
};

export default new led();

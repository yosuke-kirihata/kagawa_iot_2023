import gpio from "rpi-gpio";

function main() {
  const LED_PIN = 40;

  // LED ピンをOUT方向に設定
  gpio.setup(LED_PIN, gpio.DIR_OUT, function () {
    // LED ピンをlowに設定
    gpio.write(LED_PIN, false);
  });
}

main();

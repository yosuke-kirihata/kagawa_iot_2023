import gpio from "rpi-gpio";

async function main() {
  const LED_PIN = 40;

  // LED ピンをOUT方向に設定
  await gpio.promise.setup(LED_PIN, gpio.DIR_OUT);
  console.log("setup done.");
  // LED ピンをlowに設定
  await gpio.promise.write(LED_PIN, false);
  console.log("write done.");
}

main();

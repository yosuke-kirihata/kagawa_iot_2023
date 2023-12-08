import mqtt from "mqtt";

import led from "../lib/led";
import { CONNECT_URL, MY_TOPIC } from "../config/config";

const THRESH_PPM = 1500;

const client = mqtt.connect(CONNECT_URL);

client.on("connect", function () {
  console.log("subscriber.connected.");
});

client.subscribe(MY_TOPIC + "/sensor", function (_err, _granted) {
  console.log("subscriber.subscribed.");
});

client.on("message", function (topic, message) {
  // console.log("subscriber.on.message", "topic:", topic, "message:", message.toString());

  if (topic === MY_TOPIC + "/sensor") {
    const parsed = JSON.parse(message, function (_key, value) {
      if (typeof value === "string") {
        const valueNumber = Number(value);
        if (!Number.isNaN(valueNumber)) {
          return valueNumber;
        }
      }
      return value;
    });
    console.log(parsed.co2, parsed.temp, parsed.hum);
    if (parsed.co2 >= THRESH_PPM) {
      console.log("led on");
      led.on();
    } else {
      console.log("led off");
      led.off();
    }
  }
});

import mqtt from "mqtt";

import { CONNECT_URL } from "../config/config";

const client = mqtt.connect(CONNECT_URL);

const topic = "/kagawa/kosen/denkilab/rpi/00";
const message = "Hello MQTT!";

client.on("connect", function () {
  console.log("publisher.connected.");

  client.publish(topic, message);
  console.log("topic:", topic, ", message:", message);
});
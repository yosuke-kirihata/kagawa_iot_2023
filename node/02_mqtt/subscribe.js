import mqtt from "mqtt";

import config from "../config/config.js";

const { CONNECT_URL } = config;

const client = mqtt.connect(CONNECT_URL);

const TOPIC = "/kagawa/kosen/denkilab/rpi/00";

client.on("connect", function () {
  console.log("subscriber.connected.");
});

client.subscribe(TOPIC, function (err, granted) {
  console.log("subscriber.subscribed.");
});

client.on("message", function (topic, message) {
  console.log("subscriber.on.message", "topic:", topic, "message:", message.toString());
});

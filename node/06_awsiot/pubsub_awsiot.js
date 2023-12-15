import awsIot from "aws-iot-device-sdk";

const BASE_CERT_PATH = "../crt/";
const PRIVATE_KEY_PATH = BASE_CERT_PATH + ""; //ex: hoge-private.pem.key
const CERT_PATH = BASE_CERT_PATH + ""; //ex: fuga-certificate.pem.crt
const ROOTCA_CERT_PATH = BASE_CERT_PATH + ""; //ex: AmazonRootCA1.pem
const UUID = ""; //ex:01
const ENDPOINT = ""; //ex: piyo.iot.ap-northeast-1.amazonaws.com

const topic = "kagawa/kosen/denkilab/rpi/" + UUID;

const device = awsIot.device({
  keyPath: PRIVATE_KEY_PATH,
  certPath: CERT_PATH,
  caPath: ROOTCA_CERT_PATH,
  clientId: UUID,
  host: ENDPOINT,
});

device.on("connect", function () {
  console.log("connect");
  device.subscribe(topic);

  const message = JSON.stringify({ data: 1 });
  device.publish(topic, message);
});

device.on("message", function (topic, message) {
  console.log("message", topic, message.toString());
});

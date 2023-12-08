import { SerialPort, ReadlineParser } from "serialport";

const port = new SerialPort({
  path: "/dev/ttyACM0",
  baudRate: 115200,
  dataBits: 8,
  stopBits: 1,
  parity: "none",
});

const parser = new ReadlineParser({ delimiter: "\r\n" });
port.pipe(parser);

parser.on("data", function (data) {
  console.log(data.toString());
});

parser.on("error", function (err) {
  console.error("Error :", err);
});

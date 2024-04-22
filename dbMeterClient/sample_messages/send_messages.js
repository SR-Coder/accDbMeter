import mqtt from 'mqtt';
const sendMessageInterval = 500;
const sensors = [
    { "sensorId": 12, "sensorName": "Front of Church" },
    { "sensorId": 23, "sensorName": "Middle of Church" },
    { "sensorId": 42, "sensorName": "Back of Church" },
];
let topic = "DBMeter";
let client = mqtt.connect("mqtt://localhost:1885");
setInterval(publishMessageForEachSensor, sendMessageInterval);

function publishMessageForEachSensor() {
    sensors.forEach((sensor) => {
        let message = {};
        message.dbLevel = Math.random() * 20 + 60;
        message.timestamp = new Date().getTime();
        message.sensorId = sensor.sensorId;
        message.sensorName = sensor.sensorName;
        console.log("publishing", message);
        client.publish(topic, JSON.stringify(message), { qos: 2 }, (error) => {
            if (error) {
                console.log('Publish error: ', error)
            }
        });
    });
}

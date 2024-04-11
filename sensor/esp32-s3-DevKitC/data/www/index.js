console.log("Hello from index.js! in the Station folder");


async function getConfig() {
    const response = await fetch('/api/config');
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const config = await response.json();
    return config;
}

getConfig().then(config => {
    document.getElementById('sensor_name').value = config.sensor_name;
    document.getElementById('sensor_username').value = config.sensor_username;
    document.getElementById('sensor_password').value = config.sensor_password;
    document.getElementById('sensor_location').value = config.sensor_location;
    document.getElementById('x_loc').value = config.x_loc;
    document.getElementById('y_loc').value = config.y_loc;
    document.getElementById('mqtt_server').value = config.mqtt_server;
    document.getElementById('mqtt_port').value = config.mqtt_port;
    document.getElementById('mqtt_user').value = config.mqtt_username;
    document.getElementById('mqtt_pass').value = config.mqtt_password;
    document.getElementById('mqtt_rate').value = config.mqtt_rate;
}).catch(e => {
    console.error('Error getting config:', e);
});
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- Please use functional components

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Running the app in dev mode
`npm run dev`

## Mosquitto
Install mosquitto using:
`brew install mosquitto`

run up the server using the simple config file:
`mosquitto -c ./local.mosquitto.conf`

In the webapp, click on connect and then subscribe.

Then we can send messages using:
`mosquitto_pub -h 127.0.0.1 -p 1885 -t dbMeter/dbLevel -f sample_messages/green_low.json`

With the defaults in the webapp you should see the messages appear.

## MQTT integration

This is based on the guide here:
https://mpolinowski.github.io/docs/Development/Javascript/2021-06-01--mqtt-with-reactjs/2021-06-01/

Like the guide, the MQTT React components have been pulled in from here:
https://github.com/emqx/MQTT-Client-Examples
specifically this version:
https://github.com/emqx/MQTT-Client-Examples/tree/ccf475eec8ec7f03d6ec9e75c462fdb53bb4438d/mqtt-client-React/src/components

### TODO
[] Auth - https://mosquitto.org/documentation/authentication-methods/
# ESP8266-WS-Testing

A live WebSocket testing framework using ESP8266 microcontrollers and Django/JavaScript frontend, designed for real-time sensor data streaming and visualization.

---

## 🧠 Overview

- The **ESP8266** reads sensor data (e.g., MPU6050 accelerometer), then pushes it via WebSocket.
- A **Django Channels** server processes the WebSocket and serves data to the browser.
- The **frontend** uses Chart.js to render historical and real-time graph data, alongside a live log.

---

## 🚀 Features

- 📡 Real-time WebSocket data streaming
- 📈 Chart.js visualization: historical + live updates
- 🧠 Sensor data tracking (x, y, z axes)
- ⚙️ Dashboard-style UI with log and parameters section
- 🪄 Responsive CSS styling

---

## 🛠️ Hardware Required

| Component         | Description                          |
|-------------------|--------------------------------------|
| ESP8266 Module     | e.g., NodeMCU or Wemos D1 Mini       |
| MPU6050 IMU        | Accelerometer/Gyroscope sensor        |
| Jumper Wires       | For connecting ESP8266 and sensor    |
| Breadboard (optional) | Easy prototyping setup         |

---

## 💻 Software Setup

### ESP8266 Sketch

1. Clone the repo to Arduino's sketchbook directory.
2. Open your `.ino` file (e.g. `ws_sensor.ino`).
3. Update Wi-Fi credentials.
4. Select the correct board in Arduino IDE (e.g., *NodeMCU 1.0*).
5. Install required libraries:
   - `WebSocketsClient`
   - `Wire`
   - `Adafruit MPU6050`
6. Upload the sketch.

---

### Django Server

1. Navigate to the project folder.
2. Install Python dependencies:

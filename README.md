
# Quadruped Robot Telemetry & ML Anomaly Pipeline

This is a real-time data pipeline designed to stream and monitor health data for a 12-Degree-of-Freedom (12-DOF) quadruped robot. 

The goal of the project was to separate the hardware simulation from the backend analysis. The robot streams its joint angles at a fast 50Hz heartbeat, while an asynchronous FastAPI server uses a machine learning model to read the numbers and flag mechanical failures on the fly.


## How It Works

The system is split into three main Python scripts:

* **`train_anomaly_detector.py` (The Brain):** Generates 5,000 rows of clean baseline walking data using out-of-phase sine waves to mimic a realistic diagonal trotting gait. It trains an unsupervised **Isolation Forest** model to learn what a normal stride looks like, then saves it as a reusable binary file.
* **`telemetry_server.py` (The Backend):** A FastAPI server that loads the trained AI model straight into memory. It sets up rigid Pydantic data schemas to check incoming numbers and handles data concurrently using an `async` event loop so it doesn't freeze or drop packets.
* **`quadruped_telemetry_node.py` (The Simulator):** Acts as the physical robot chassis. It calculates 12 joint positions every 20ms and fires them over local network sockets using HTTP POST requests. It also has a random trigger that injects sudden, severe noise to simulate slips, trips, or motor jams to test if the server catches it.



## Network Data Schema

Data is serialized into JSON payloads before being pushed across the network socket:

* `packet_id` (int): Tracks packet order and data drop rates.
* `timestamp` (float): Tracks exact runtime at the edge.
* `joints` (object): Maps coordinates for all 12 joints (Hip, Thigh, Knee across 4 legs).



## Getting Started

### Dependencies
Install the required Python modules:
```bash
pip install fastapi pydantic uvicorn scikit-learn pandas requests numpy
1. Training the ai model-python train_anomaly_detector.py
2. API server listener-python telemetry_server.py
3. Robot simulation-python quadruped_telemetry_node.py

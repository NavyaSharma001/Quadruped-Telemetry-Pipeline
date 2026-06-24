import time
import json
import math
import random

def generate_trot_gait_telemetry():
    """
    Simulates high-frequency 12-DOF kinematics telemetry for a quadruped robot
    Leg Layout: Front-Left (FL), Front-Right (FR), Rear-Left (RL), Rear-Right (RR)
    Each leg has 3 joints: Hip, Thigh, Knee
    """
    start_time = time.time()
    packet_id = 0
    
    # Base gait configurations
    frequency = 1.5  # Stride cycles per second (Hz)
    
    print(">> Initializing Quadruped Telemetry Node streaming at 50Hz...")
    
    try:
        while True:
            t = time.time() - start_time
            packet_id += 1
            
            # Formulate leg phase offsets (Trot gait: Diagonal pairs move together)
            phase_pair_1 = math.sin(2 * math.pi * frequency * t)
            phase_pair_2 = math.sin(2 * math.pi * frequency * t + math.pi) # 180 deg out of phase
            
            # Inject random micro-anomalies to simulate physical joint friction / resistance
            anomaly_trigger = random.random()
            noise_factor = 0.5 if anomaly_trigger > 0.98 else 0.02
            
            # Structural state dictionary payload mapping physical joint parameters
            telemetry_payload = {
                "packet_id": packet_id,
                "timestamp": round(t, 4),
                "system_status": "CRITICAL_ANOMALY" if noise_factor > 0.1 else "HEALTHY",
                "joints": {
                    # Pair 1: Front-Left and Rear-Right legs
                    "FL_hip":   round(0.1 * phase_pair_1 + random.gauss(0, noise_factor), 4),
                    "FL_thigh": round(0.4 * phase_pair_1 + random.gauss(0, noise_factor), 4),
                    "FL_knee":  round(-0.6 * phase_pair_1 + random.gauss(0, noise_factor), 4),
                    "RR_hip":   round(0.1 * phase_pair_1 + random.gauss(0, noise_factor), 4),
                    "RR_thigh": round(0.4 * phase_pair_1 + random.gauss(0, noise_factor), 4),
                    "RR_knee":  round(-0.6 * phase_pair_1 + random.gauss(0, noise_factor), 4),
                    
                    # Pair 2: Front-Right and Rear-Left legs
                    "FR_hip":   round(0.1 * phase_pair_2 + random.gauss(0, noise_factor), 4),
                    "FR_thigh": round(0.4 * phase_pair_2 + random.gauss(0, noise_factor), 4),
                    "FR_knee":  round(-0.6 * phase_pair_2 + random.gauss(0, noise_factor), 4),
                    "RL_hip":   round(0.1 * phase_pair_2 + random.gauss(0, noise_factor), 4),
                    "RL_thigh": round(0.4 * phase_pair_2 + random.gauss(0, noise_factor), 4),
                    "RL_knee":  round(-0.6 * phase_pair_2 + random.gauss(0, noise_factor), 4)
                }
            }
            
            # Pretty print the payload to console
            print(json.dumps(telemetry_payload))
            
            # Maintain a strict 50Hz hardware loop cycle (20ms step intervals)
            time.sleep(0.02)
            
    except KeyboardInterrupt:
        print("\n>> Telemetry stream terminated safely.")

if __name__ == "__main__":
    generate_trot_gait_telemetry()

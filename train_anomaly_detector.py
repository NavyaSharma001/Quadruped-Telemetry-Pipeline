# Run first: pip install scikit-learn pandas
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest
def train_gait_model():
    print(">> Generating clean baseline training data...")
    np.random.seed(42)
     # Simulate 5,000 packets of perfectly healthy, smooth trot gait cycles
    t = np.linspace(0, 100, 5000)
    phase_1 = np.sin(2 * np.pi * 1.5 * t)
    phase_2 = np.sin(2 * np.pi * 1.5 * t + np.pi)
     # Map physical 12-DOF joint constraints with standard baseline noise
    data = {
        "FL_hip":   0.1 * phase_1 + np.random.normal(0, 0.02, 5000),
        "FL_thigh": 0.4 * phase_1 + np.random.normal(0, 0.02, 5000),
        "FL_knee": -0.6 * phase_1 + np.random.normal(0, 0.02, 5000),
        "RR_hip":   0.1 * phase_1 + np.random.normal(0, 0.02, 5000),
        "RR_thigh": 0.4 * phase_1 + np.random.normal(0, 0.02, 5000),
        "RR_knee": -0.6 * phase_1 + np.random.normal(0, 0.02, 5000),
        "FR_hip":   0.1 * phase_2 + np.random.normal(0, 0.02, 5000),
        "FR_thigh": 0.4 * phase_2 + np.random.normal(0, 0.02, 5000),
        "FR_knee": -0.6 * phase_2 + np.random.normal(0, 0.02, 5000),
        "RL_hip":   0.1 * phase_2 + np.random.normal(0, 0.02, 5000),
        "RL_thigh": 0.4 * phase_2 + np.random.normal(0, 0.02, 5000),
        "RL_knee": -0.6 * phase_2 + np.random.normal(0, 0.02, 5000)
    }
     df = pd.DataFrame(data)
    print(">> Training Unsupervised Isolation Forest Anomaly Detection AI...")
    # contamination=0.01 means we expect roughly 1% noise in the baseline data
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(df)
    # Save the trained AI brain as a reusable file
    with open("quadruped_model.pkl", "wb") as f:
        pickle.dump(model, f)
        print(">> AI model successfully trained and saved to 'quadruped_model.pkl'!")

if __name__ == "__main__":
    train_gait_model()

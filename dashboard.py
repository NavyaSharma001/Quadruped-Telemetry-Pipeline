import streamlit as st
import pandas as pd
import numpy as np
import time

# make it fill the whole monitor
st.set_page_config(page_title="Quadruped Mission Control", layout="wide")

st.title("🤖 Quadruped Robot Telemetry & ML Diagnostics")
st.markdown("Real-time 12-DOF Joint Streams & Machine Learning Anomaly Detection Gateway")

# left side for stats, right side for the big graph
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 System Status")
    alert_placeholder = st.empty()
    packet_metric = st.metric(label="Packets Processed", value="0")
    
    st.subheader("🦿 Live Joint Readouts")
    table_placeholder = st.empty()

with col2:
    st.subheader("📈 Real-Time Kinematics Waveforms (12-DOF)")
    chart_placeholder = st.empty()

# 50 frames buffer for the sliding chart window
max_frames = 50
joint_names = [
    "FL_hip", "FL_thigh", "FL_knee",
    "FR_hip", "FR_thigh", "FR_knee",
    "RL_hip", "RL_thigh", "RL_knee",
    "RR_hip", "RR_thigh", "RR_knee"
]
# start everything at 0.0
df_buffer = pd.DataFrame(0.0, index=np.arange(max_frames), columns=joint_names)

packet_idx = 0
t_clock = 0

# main streaming loop
while True:
    t_clock += 0.04
    packet_idx += 1
    
    # math for the diagonal trotting gait (1.5 Hz frequency)
    wave_a = np.sin(2 * np.pi * 1.5 * t_clock)
    wave_b = np.sin(2 * np.pi * 1.5 * t_clock + np.pi) # 180 deg out of phase
    
    # 3% chance the dog slips or hits something
    roll_dice = np.random.rand()
    fault_triggered = roll_dice > 0.97
    noise_level = 0.6 if fault_triggered else 0.02
    
    packet_data = {}
    for joint in joint_names:
        # sync opposing leg pairs
        current_wave = wave_a if ("FL" in joint or "RR" in joint) else wave_b
        
        # scale down hips, scale up knees
        if "hip" in joint:
            multiplier = 0.1
        elif "thigh" in joint:
            multiplier = 0.4
        else:
            multiplier = -0.6
            
        packet_data[joint] = round(multiplier * current_wave + np.random.normal(0, noise_level), 4)
        
    # push new row to bottom, kick oldest row off the top
    latest_row = pd.DataFrame([packet_data])
    df_buffer = pd.concat([df_buffer, latest_row], ignore_index=True).iloc[1:]
    
    # push everything to the web screen
    chart_placeholder.line_chart(df_buffer)
    packet_metric.metric(label="Packets Processed", value=str(packet_idx))
    table_placeholder.dataframe(pd.DataFrame(list(packet_data.items()), columns=["Joint", "Radians"]), height=300)
    
    # update the warning flag box
    if fault_triggered:
        alert_placeholder.error("🚨 CRITICAL ANOMALY DETECTED (-1)\n\nTriggering Emergency Stop Packet!")
        time.sleep(0.8) # stall so the flash is visible
    else:
        alert_placeholder.success("🟢 SYSTEM HEALTHY (1)\n\nGait Pattern Within Normal ML Bounds")
        
    time.sleep(0.02) # loop at roughly 50Hz

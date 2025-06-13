
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

st.title("🌪️ Coriolis Force Simulation")
st.write("Visualizing the effect of the Coriolis force caused by Earth's rotation.")

# User inputs
v0 = st.slider("Initial Velocity Northward (m/s)", 10, 200, 50, step=5)  # 속도 최대값 늘림
hemisphere = st.radio("Hemisphere", ("Northern Hemisphere", "Southern Hemisphere"))

# Simulation parameters
omega = 7.29e-5  # Earth's angular velocity (rad/s)
dt = 10          # 시간 간격 줄여서 더 정밀하게 (원래 100 -> 10)
duration = 30000 # 전체 시뮬레이션 시간 줄임 (150000 -> 30000)
steps = int(duration / dt)

r = np.array([0.0, 0.0])
v = np.array([0.0, v0])
trajectory = []
forces = []

for _ in range(steps):
    sign = -1 if hemisphere == "Northern Hemisphere" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])
    v += coriolis * dt
    r += v * dt
    trajectory.append(r.copy())
    forces.append(coriolis.copy())

trajectory = np.array(trajectory)
forces = np.array(forces)

# Visualization
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(trajectory[:, 0], trajectory[:, 1], label="Air Trajectory", color="green")

# 화살표 간격 조정 (간격 줄여서 더 많이 표시)
arrow_step = max(1, steps // 50)
for i in range(0, len(trajectory), arrow_step):
    ax.quiver(
        trajectory[i, 0], trajectory[i, 1],
        forces[i, 0], forces[i, 1],
        color="red", scale_units="xy", scale=1e-3, width=0.003
    )

ax.set_title(f"Coriolis Force Effect on Air Trajectory ({hemisphere})")
ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.legend()
ax.grid(True)
st.pyplot(fig)
ax.set_xlabel("동서 방향 거리 (m)")
ax.set_ylabel("남북 방향 거리 (m)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

st.title("🌍 Coriolis Force Simulation")
st.write("The simulation shows how Coriolis force affects an object moving on Earth.")

# 초기 속도 크기와 방향 입력
v0_mag = st.slider("Initial speed magnitude (m/s)", 1, 100, 50, step=1)
v0_angle_deg = st.slider("Initial velocity direction (degrees from North, clockwise)", 0, 360, 0, step=1)
hemisphere = st.radio("Select Hemisphere", ("Northern", "Southern"))

omega = 7.29e-5  # rad/s
dt = 10
duration = 2000  # 총 시뮬레이션 시간
steps = int(duration / dt)

# 초기 속도 벡터 계산 (0도 = 북쪽, 90도 = 동쪽)
angle_rad = np.deg2rad(v0_angle_deg)
v = np.array([
    v0_mag * np.sin(angle_rad),  # 동서 속도 (x)
    v0_mag * np.cos(angle_rad)   # 남북 속도 (y)
])
r = np.array([0.0, 0.0])

trajectory = []
positions_for_arrows = []
forces_for_arrows = []

for i in range(steps):
    sign = -1 if hemisphere == "Northern" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])
    v += coriolis * dt
    r += v * dt

    trajectory.append(r.copy())

    if i % (steps // 10) == 0:
        positions_for_arrows.append(r.copy())
        forces_for_arrows.append(coriolis.copy() * 1e7)  # 힘 벡터 크게 확대

trajectory = np.array(trajectory)
positions_for_arrows = np.array(positions_for_arrows)
forces_for_arrows = np.array(forces_for_arrows)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(trajectory[:, 0], trajectory[:, 1], label=f"Trajectory (speed={v0_mag} m/s, angle={v0_angle_deg}°)", color="blue")
ax.scatter(trajectory[:, 0], trajectory[:, 1], s=10, alpha=0.5, color='blue')

ax.quiver(
    positions_for_arrows[:, 0], positions_for_arrows[:, 1],
    forces_for_arrows[:, 0], forces_for_arrows[:, 1],
    color="red", scale_units="xy", scale=1, width=0.007, alpha=0.8,
    label="Coriolis force"
)

margin = 500
ax.set_xlim(np.min(trajectory[:, 0]) - margin, np.max(trajectory[:, 0]) + margin)
ax.set_ylim(np.min(trajectory[:, 1]) - margin, np.max(trajectory[:, 1]) + margin)

ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.set_title(f"Coriolis Force Trajectory ({hemisphere} Hemisphere)")
ax.grid(True)
ax.legend()

st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit 설정
st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

st.title("🌍 Coriolis Force Simulation")
st.write("Visualizing the Coriolis effect on an air parcel due to Earth's rotation.")

# 사용자 입력
v0 = st.slider("Initial northward velocity (m/s)", 10, 300, 50, step=10)
hemisphere = st.radio("Select Hemisphere", ("Northern", "Southern"))

# 시뮬레이션 파라미터
omega = 7.29e-5  # 지구 자전 각속도 [rad/s]
dt = 10
duration = 100000
steps = int(duration / dt)

# 초기값
r = np.array([0.0, 0.0])       # 초기 위치
v = np.array([0.0, v0])        # 초기 속도
trajectory = []
forces = []

# 시뮬레이션 루프
for _ in range(steps):
    sign = -1 if hemisphere == "Northern" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])
    v += coriolis * dt
    r += v * dt
    trajectory.append(r.copy())
    forces.append(coriolis.copy())

trajectory = np.array(trajectory)
forces = np.array(forces)

# 시각화
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(trajectory[:, 0], trajectory[:, 1], label=f"Trajectory (v₀={v0} m/s)", color="blue")

# 코리올리 화살표 벡터
for i in range(0, len(trajectory), steps // 50):
    ax.quiver(
        trajectory[i, 0], trajectory[i, 1],
        forces[i, 0], forces[i, 1],
        color="crimson", scale_units="xy", scale=1e-6, width=0.003,
        alpha=0.8
    )

# 축 및 제목
ax.set_title(f"Trajectory Affected by Coriolis Force ({hemisphere} Hemisphere)")
ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.grid(True)
ax.legend()

# Streamlit 출력
st.pyplot(fig)

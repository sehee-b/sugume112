import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

# 제목
st.title("🌍 Coriolis Force Simulation")
st.write("This simulation shows the Coriolis force affecting a moving object due to Earth's rotation.")

# 사용자 입력
v0 = st.slider("Initial northward velocity (m/s)", 10, 300, 50, step=10)
hemisphere = st.radio("Select Hemisphere", ("Northern", "Southern"))

# 파라미터 설정
omega = 7.29e-5  # rad/s
dt = 10          # 시간 간격
duration = 20000  # 시뮬레이션 시간
steps = int(duration / dt)

# 초기값
r = np.array([0.0, 0.0])   # 위치
v = np.array([0.0, v0])    # 속도
trajectory = []
forces = []
positions_for_arrows = []
forces_for_arrows = []

# 시뮬레이션
for i in range(steps):
    sign = -1 if hemisphere == "Northern" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])
    v += coriolis * dt
    r += v * dt
    trajectory.append(r.copy())
    forces.append(coriolis.copy())

    # 일정 간격마다 화살표 저장
    if i % (steps // 10) == 0:
        positions_for_arrows.append(r.copy())
        forces_for_arrows.append(coriolis.copy() * 1e6)  # 스케일 조정해서 크게 보이게!

trajectory = np.array(trajectory)
positions_for_arrows = np.array(positions_for_arrows)
forces_for_arrows = np.array(forces_for_arrows)

# 시각화
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(trajectory[:, 0], trajectory[:, 1], label=f"Trajectory (v₀={v0} m/s)", color="blue")

# 코리올리 화살표 (눈에 확 띄게 확대!)
ax.quiver(
    positions_for_arrows[:, 0], positions_for_arrows[:, 1],
    forces_for_arrows[:, 0], forces_for_arrows[:, 1],
    color="red", scale_units="xy", scale=1, width=0.005, alpha=0.8,
    label="Coriolis force"
)

# 축 설정
ax.set_title(f"Trajectory and Coriolis Force Vectors ({hemisphere} Hemisphere)")
ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.grid(True)
ax.legend()

# 출력
st.pyplot(fig)

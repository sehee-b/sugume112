import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

# 제목
st.title("🌍 Coriolis Force Simulation")
st.write("Visualizing the Coriolis effect on a moving air parcel due to Earth's rotation.")

# 사용자 입력
v0 = st.slider("Initial northward velocity (m/s)", 10, 300, 50, step=10)
hemisphere = st.radio("Select Hemisphere", ("Northern", "Southern"))

# 시뮬레이션 파라미터
omega = 7.29e-5  # 지구 자전 각속도 [rad/s]
dt = 10          # 시간 간격
duration = 100000  # 총 시뮬레이션 시간 [s]
steps = int(duration / dt)

# 초기 위치 및 속도
r = np.array([0.0, 0.0])  # 초기 위치 [x, y]
v = np.array([0.0, v0])   # 초기 속도 [vx, vy]
trajectory = []
forces = []

# 궤적 계산
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

# 코리올리 힘 벡터 표시 (화살표)
for i in range(0, len(trajectory), steps // 30):
    ax.quiver(
        trajectory[i, 0], trajectory[i, 1],
        forces[i, 0], forces[i, 1],
        color="red", scale_units="xy", scale=1e-3, width=0.002
    )

# 축 자동 조정
x_min, x_max = trajectory[:, 0].min(), trajectory[:, 0].max()
y_min, y_max = trajectory[:, 1].min(), trajectory[:, 1].max()
x_margin = (x_max - x_min) * 0.1
y_margin = (y_max - y_min) * 0.1
ax.set_xlim(x_min - x_margin, x_max + x_margin)
ax.set_ylim(y_min - y_margin, y_max + y_margin)

# 그래프 설정
ax.set_title(f"Trajectory Affected by Coriolis Force ({hemisphere} Hemisphere)")
ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.grid(True)
ax.legend()

# 결과 출력
st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

# 제목
st.title("🌍 Coriolis Force Simulation")
st.write("This simulation shows the Coriolis force affecting a moving object due to Earth's rotation.")

# 사용자 입력 (속도 범위를 1~100으로 줄이고 세밀하게 조절 가능하게)
v0 = st.slider("Initial northward velocity (m/s)", 1, 100, 50, step=1)
hemisphere = st.radio("Select Hemisphere", ("Northern", "Southern"))

# 파라미터 설정
omega = 7.29e-5  # rad/s
dt = 30          # 시간 간격 (조금 키워서 눈에 띄게)
duration = 6000  # 시뮬레이션 시간 (조금 줄임)
steps = int(duration / dt)

# 초기값
r = np.array([0.0, 0.0])   # 위치
v = np.array([0.0, v0])    # 속도 (동서=0, 남북=v0)
trajectory = []
forces = []
positions_for_arrows = []
forces_for_arrows = []

for i in range(steps):
    sign = -1 if hemisphere == "Northern" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])  # 코리올리 가속도 벡터
    v += coriolis * dt
    r += v * dt
    trajectory.append(r.copy())
    forces.append(coriolis.copy())

    # 10등분해서 화살표 위치 및 힘 저장
    if i % (steps // 10) == 0:
        positions_for_arrows.append(r.copy())
        # 힘 벡터 크기를 좀 더 크게 확대 (스케일 = 5e6 -> 1e7)
        forces_for_arrows.append(coriolis.copy() * 1e7)

trajectory = np.array(trajectory)
positions_for_arrows = np.array(positions_for_arrows)
forces_for_arrows = np.array(forces_for_arrows)

# 시각화
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(trajectory[:, 0], trajectory[:, 1], label=f"Trajectory (v₀={v0} m/s)", color="blue")

# 궤적 포인트 표시 (작은 점)
ax.scatter(trajectory[:, 0], trajectory[:, 1], s=5, color='blue', alpha=0.3)

# 코리올리 힘 화살표
ax.quiver(
    positions_for_arrows[:, 0], positions_for_arrows[:, 1],
    forces_for_arrows[:, 0], forces_for_arrows[:, 1],
    color="red", scale_units="xy", scale=1, width=0.007, alpha=0.9,
    label="Coriolis force"
)

# 축 범위 자동설정 (궤적 중심 기준 ± 마진)
margin = 1000
ax.set_xlim(np.min(trajectory[:, 0]) - margin, np.max(trajectory[:, 0]) + margin)
ax.set_ylim(np.min(trajectory[:, 1]) - margin, np.max(trajectory[:, 1]) + margin)

ax.set_title(f"Trajectory and Coriolis Force Vectors ({hemisphere} Hemisphere)")
ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.grid(True)
ax.legend()

st.pyplot(fig)

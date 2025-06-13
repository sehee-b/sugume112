
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="코리올리 힘 시뮬레이션", layout="centered")

st.title("🌪️ 코리올리 힘 시뮬레이션")
st.write("지구 자전에 의해 발생하는 코리올리 힘의 영향을 시각화합니다.")

# 사용자 입력
v0 = st.slider("초기 속도 (북쪽, m/s)", 10, 100, 50, step=5)
hemisphere = st.radio("반구 선택", ("북반구", "남반구"))

# 시뮬레이션 파라미터
omega = 7.29e-5  # 지구 자전 각속도
dt = 100
duration = 150000
steps = int(duration / dt)
r = np.array([0.0, 0.0])
v = np.array([0.0, v0])
trajectory = []
forces = []

for _ in range(steps):
    sign = -1 if hemisphere == "북반구" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])
    v += coriolis * dt
    r += v * dt
    trajectory.append(r.copy())
    forces.append(coriolis.copy())

trajectory = np.array(trajectory)
forces = np.array(forces)

# 시각화
fig, ax = plt.subplots(figsize=(6, 5))
ax.plot(trajectory[:, 0], trajectory[:, 1], label="공기 궤적", color="green")
for i in range(0, len(trajectory), 500):
    ax.quiver(
        trajectory[i, 0], trajectory[i, 1],
        forces[i, 0], forces[i, 1],
        color="red", scale_units="xy", scale=1e-3, width=0.003
    )
ax.set_title(f"코리올리 힘에 따른 공기 궤적 ({hemisphere})")
ax.set_xlabel("동서 방향 거리 (m)")
ax.set_ylabel("남북 방향 거리 (m)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coriolis Force Simulation", layout="centered")

st.title("🌍 Coriolis Force Simulation")
st.write("Visualizing the Coriolis force due to Earth's rotation.")

# User inputs
v0 = st.slider("Initial northward velocity (m/s)", 10, 300, 50, step=10)
hemisphere = st.radio("Select Hemisphere", ("Northern", "Southern"))

# Simulation parameters
omega = 7.29e-5  # Earth's angular speed [rad/s]
dt = 10          # Time step
duration = 100000  # Total time
steps = int(duration / dt)

# Initialize
r = np.array([0.0, 0.0])  # position
v = np.array([0.0, v0])   # initial velocity
trajectory = []
forces = []

for _ in range(steps):
    sign = -1 if hemisphere == "Northern" else 1
    coriolis = sign * 2 * omega * np.array([-v[1], v[0]])
    v += coriolis * dt
    r += v * dt
    trajectory.append(r.copy())
    forces.append(coriolis.copy())

trajectory = np.array(trajectory)
forces = np.array(forces)

# Plotting
fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(trajectory[:, 0], trajectory[:, 1], label="Trajectory", color="blue")

# Draw Coriolis force arrows
for i in range(0, len(trajectory), steps // 30):
    ax.quiver(
        trajectory[i, 0], trajectory[i, 1],
        forces[i, 0], forces[i, 1],
        color="red", scale_units="xy", scale=1e-3, width=0.002
    )

ax.set_title(f"Trajectory Affected by Coriolis Force ({hemisphere} Hemisphere)")
ax.set_xlabel("East-West Distance (m)")
ax.set_ylabel("North-South Distance (m)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

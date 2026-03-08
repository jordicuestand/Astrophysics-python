# ============================================================
#02_stellar_parallax.py
# ============================================================
import os
import numpy as np
import matplotlib.pyplot as plt

print("RUNNING:", os.path.abspath(__file__))


# ============================================================
# 1. Physical constants
# ============================================================

AU = 1.495978707e11       # m, astronomical unit
PC = 3.085677581e16       # m, parsec
RAD_TO_ARCSEC = 206264.80624709636


# ============================================================
# 2. User parameters
# ============================================================

distance_pc = 10.0        # Distance to the star in parsecs
beta_deg = 45.0           # Ecliptic latitude of the star in degrees
n_points = 500            # Number of samples along Earth's orbit


# ============================================================
# 3. Derived quantities
# ============================================================

distance = distance_pc * PC
beta = np.radians(beta_deg)

# Theoretical parallax in arcseconds
p_theory_arcsec = 1.0 / distance_pc


# ============================================================
# 4. Earth's orbit around the Sun
# ============================================================

t = np.linspace(0.0, 2.0 * np.pi, n_points)

x_earth = AU * np.cos(t)
y_earth = AU * np.sin(t)
z_earth = np.zeros_like(t)


# ============================================================
# 5. Star position in space
# ============================================================

# We choose ecliptic longitude lambda = 0 for simplicity.
x_star = distance * np.cos(beta)
y_star = 0.0
z_star = distance * np.sin(beta)

star_vector = np.array([x_star, y_star, z_star])
u0 = star_vector / np.linalg.norm(star_vector)


# ============================================================
# 6. Apparent direction from Earth to the star
# ============================================================

dx = x_star - x_earth
dy = y_star - y_earth
dz = z_star - z_earth

r_obs = np.vstack((dx, dy, dz)).T
norms = np.linalg.norm(r_obs, axis=1)
u_obs = r_obs / norms[:, None]


# ============================================================
# 7. Local orthonormal basis on the sky
# ============================================================

k = np.array([0.0, 0.0, 1.0])

if np.linalg.norm(np.cross(k, u0)) < 1e-12:
    k = np.array([0.0, 1.0, 0.0])

e1 = np.cross(k, u0)
e1 = e1 / np.linalg.norm(e1)

e2 = np.cross(u0, e1)
e2 = e2 / np.linalg.norm(e2)


# ============================================================
# 8. Angular displacement in the tangent plane
# ============================================================

delta = u_obs - u0

xi = delta @ e1
eta = delta @ e2

xi_arcsec = xi * RAD_TO_ARCSEC
eta_arcsec = eta * RAD_TO_ARCSEC


# ============================================================
# 9. Informative output
# ============================================================

semi_width = 0.5 * (xi_arcsec.max() - xi_arcsec.min())
semi_height = 0.5 * (eta_arcsec.max() - eta_arcsec.min())

print("Distance to the star (pc):", distance_pc)
print("Ecliptic latitude beta (deg):", beta_deg)
print("Theoretical parallax (arcsec):", p_theory_arcsec)
print("Horizontal semi-axis (arcsec):", semi_width)
print("Vertical semi-axis (arcsec):", semi_height)


# ============================================================
# 10. Plot: geometry + apparent motion
# ============================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

# ------------------------------------------------------------
# Left panel: physical geometry (not to scale)
# ------------------------------------------------------------

orbit_scale = AU
star_scale = 3.0 * AU   # purely visual compression for plotting

x_star_plot = star_scale * np.cos(beta)
z_star_plot = star_scale * np.sin(beta)

# ------------------------------------------------------------
# Small schematic parallax ellipse around the star (not to scale)
# ------------------------------------------------------------

ellipse_size = 0.1 * AU  # purely illustrative scale

phi = np.linspace(0, 2*np.pi, 200)

ellipse_x = x_star_plot + ellipse_size * np.cos(phi)
ellipse_y = z_star_plot + ellipse_size * np.sin(beta) * np.sin(phi)

ax1.plot(ellipse_x / AU, ellipse_y / AU, linestyle=":", linewidth=1.5)

# Earth's orbit in the x-y plane (shown edge-on as x vs y)
ax1.plot(x_earth / AU, y_earth / AU, label="Earth's orbit")
ax1.plot(0, 0, "o", label="Sun")
ax1.plot(x_star_plot / AU, z_star_plot / AU, "*", markersize=12, label="Star")

# Two Earth positions six months apart
idx1 = 0
idx2 = n_points // 2

ax1.plot(x_earth[idx1] / AU, y_earth[idx1] / AU, "o")
ax1.plot(x_earth[idx2] / AU, y_earth[idx2] / AU, "o")

# Sight lines to the star (schematic)
ax1.plot(
    [x_earth[idx1] / AU, x_star_plot / AU],
    [y_earth[idx1] / AU, z_star_plot / AU],
    "--"
)
ax1.plot(
    [x_earth[idx2] / AU, x_star_plot / AU],
    [y_earth[idx2] / AU, z_star_plot / AU],
    "--"
)

ax1.set_aspect("equal", adjustable="box")
ax1.grid(True)
ax1.set_xlabel("x (AU)")
ax1.set_ylabel("y / projected height (AU)")
ax1.set_title("Geometric origin of stellar parallax")
ax1.legend()

# ------------------------------------------------------------
# Right panel: apparent motion on the sky
# ------------------------------------------------------------

ax2.plot(
    xi_arcsec,
    eta_arcsec,
    linestyle="--",
    linewidth=2,
    label="Parallax ellipse"
)
ax2.plot(xi_arcsec[0], eta_arcsec[0], "o", label="Starting point")

ax2.set_aspect("equal", adjustable="box")
ax2.grid(True)
ax2.set_xlabel("Angular displacement along e1 (arcsec)")
ax2.set_ylabel("Angular displacement along e2 (arcsec)")
ax2.set_title("Apparent motion on the sky")
ax2.legend()

plt.tight_layout()
plt.show()
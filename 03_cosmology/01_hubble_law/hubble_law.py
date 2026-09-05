"""
Hubble's Law - Simple observational simulation
------------------------------------------------

This script simulates a set of galaxies following Hubble's law

    v = H0 * d

and adds random peculiar velocities to mimic real observations.

From the simulated data, the script estimates the Hubble constant H0
and calculates the corresponding Hubble radius and Hubble time.

The goal is to illustrate how the global expansion of the Universe
emerges from observational data despite local velocity deviations.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# USER PARAMETERS
# ============================================================

H0 = 70.0                  # Hubble constant [km/s/Mpc]

n_galaxies = 50            # Number of simulated galaxies
min_distance = 5.0         # Minimum galaxy distance [Mpc]
max_distance = 200.0       # Maximum galaxy distance [Mpc]

peculiar_sigma = 250.0     # Typical peculiar velocity dispersion [km/s]

random_seed = 42           # Makes the simulation reproducible

save_figure = True
output_filename = "images/hubble_law_example.png"


# ============================================================
# PHYSICAL CONSTANTS
# ============================================================

c = 299792.458              # Speed of light [km/s]

MPC_IN_KM = 3.085677581e19
SECONDS_PER_YEAR = 365.25 * 24 * 3600


# ============================================================
# GENERATE A SIMULATED GALAXY SAMPLE
# ============================================================

rng = np.random.default_rng(random_seed)

# Random galaxy distances
distance = rng.uniform(
    min_distance,
    max_distance,
    n_galaxies
)

# Sort distances only to make plots easier to read
distance.sort()

# Ideal recession velocity from Hubble's law
velocity_hubble = H0 * distance

# Random peculiar velocities
peculiar_velocity = rng.normal(
    loc=0.0,
    scale=peculiar_sigma,
    size=n_galaxies
)

# "Observed" recession velocity
velocity_observed = velocity_hubble + peculiar_velocity


# ============================================================
# ESTIMATE H0 FROM THE SIMULATED OBSERVATIONS
# ============================================================

# Least-squares fit constrained to pass through the origin:
#
#     v = H0_fit * d
#
# For this model:
#
#     H0_fit = sum(d * v) / sum(d^2)

H0_fit = np.sum(distance * velocity_observed) / np.sum(distance**2)

velocity_fit = H0_fit * distance

residuals = velocity_observed - velocity_fit


# ============================================================
# HUBBLE RADIUS
# ============================================================

# R_H = c / H0
#
# Because c is in km/s and H0 in km/s/Mpc,
# the result is directly obtained in Mpc.

hubble_radius_mpc = c / H0_fit

hubble_radius_billion_ly = (
    hubble_radius_mpc * 3.26156 / 1000
)


# ============================================================
# HUBBLE TIME
# ============================================================

# t_H = 1 / H0
#
# First convert H0 from km/s/Mpc to s^-1.

H0_si = H0_fit / MPC_IN_KM

hubble_time_seconds = 1.0 / H0_si

hubble_time_billion_years = (
    hubble_time_seconds
    / SECONDS_PER_YEAR
    / 1e9
)


# ============================================================
# PRINT RESULTS
# ============================================================

difference_percent = 100 * (H0_fit - H0) / H0

print()
print("HUBBLE LAW SIMULATION")
print("---------------------")
print(f"Input H0:             {H0:.2f} km/s/Mpc")
print(f"Estimated H0:         {H0_fit:.2f} km/s/Mpc")
print(f"Difference:           {difference_percent:+.2f} %")
print()
print(f"Hubble radius:        {hubble_radius_mpc:.0f} Mpc")
print(
    f"Hubble radius:        "
    f"{hubble_radius_billion_ly:.2f} billion light-years"
)
print(
    f"Hubble time:          "
    f"{hubble_time_billion_years:.2f} billion years"
)
print()


# ============================================================
# PLOT
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)

# ------------------------------------------------------------
# Left panel: Hubble diagram
# ------------------------------------------------------------

ax1.scatter(
    distance,
    velocity_observed,
    label="Simulated galaxies"
)

ax1.plot(
    distance,
    velocity_hubble,
    linestyle="--",
    label=f"Input law: H₀ = {H0:.1f}"
)

ax1.plot(
    distance,
    velocity_fit,
    label=f"Best fit: H₀ = {H0_fit:.1f}"
)

# Show the characteristic scale of peculiar velocities
ax1.fill_between(
    distance,
    velocity_fit - peculiar_sigma,
    velocity_fit + peculiar_sigma,
    alpha=0.15,
    label=f"±1σ peculiar velocity ({peculiar_sigma:.0f} km/s)"
)

ax1.set_xlabel("Distance [Mpc]")
ax1.set_ylabel("Recession velocity [km/s]")
ax1.set_title("Hubble diagram")
ax1.legend()
ax1.grid(alpha=0.3)

ax1.text(
    0.04,
    0.96,
    "Galaxies do not fall exactly on a straight line,\n"
    "but the global distance–velocity relation\n"
    "emerges clearly from the data.",
    transform=ax1.transAxes,
    va="top",
    fontsize=9,
    bbox=dict(boxstyle="round", alpha=0.8)
)


# ------------------------------------------------------------
# Right panel: residual velocities
# ------------------------------------------------------------

ax2.scatter(
    distance,
    residuals
)

ax2.axhline(
    0,
    linestyle="--"
)

# Characteristic peculiar-velocity scale
ax2.axhline(
    peculiar_sigma,
    linestyle=":",
    alpha=0.7
)

ax2.axhline(
    -peculiar_sigma,
    linestyle=":",
    alpha=0.7
)

ax2.set_xlabel("Distance [Mpc]")
ax2.set_ylabel("Observed − predicted velocity [km/s]")
ax2.set_title("Residuals — vertical zoom")
ax2.grid(alpha=0.3)

ax2.text(
    0.04,
    0.96,
    "Subtracting the predicted Hubble velocity\n"
    "leaves mainly the simulated peculiar velocities.\n"
    "The vertical scale is strongly magnified.",
    transform=ax2.transAxes,
    va="top",
    fontsize=9,
    bbox=dict(boxstyle="round", alpha=0.8)
)

# ============================================================
# SAVE FIGURE
# ============================================================

if save_figure:
    output_directory = os.path.dirname(output_filename)

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    plt.savefig(
        output_filename,
        dpi=150,
        bbox_inches="tight"
    )

    print(f"Figure saved as: {output_filename}")


plt.show()
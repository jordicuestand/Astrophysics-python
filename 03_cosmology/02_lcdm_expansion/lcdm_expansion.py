"""
Expansion history of a Lambda-CDM Universe
------------------------------------------

This script explores how the expansion rate of the Universe changes
with the scale factor a in a simplified flat Lambda-CDM cosmology.

The model contains three components:

    radiation
    matter
    dark energy (cosmological constant)

The Friedmann equation is written as

    H(a)^2 / H0^2 =
        Omega_r / a^4
        + Omega_m / a^3
        + Omega_lambda

The script shows:

1. How H(a) changes as the Universe expands.
2. How the relative importance of radiation, matter and dark energy
   changes with the scale factor.

The present Universe corresponds to a = 1.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# USER PARAMETERS
# ============================================================

H0 = 70.0                 # Present Hubble constant [km/s/Mpc]

Omega_r = 9.0e-5          # Radiation density parameter
Omega_m = 0.3            # Matter density parameter
Omega_lambda = 0.70       # Dark-energy density parameter

a_min = 1.0e-6               # Earliest scale factor shown
a_max = 10.0               # Also show part of the future
n_points = 2000

save_figure = True
output_filename = "images/lcdm_expansion_example.png"


# ============================================================
# CHECK THE COSMOLOGICAL PARAMETERS
# ============================================================

Omega_total = Omega_r + Omega_m + Omega_lambda

print()
print("LAMBDA-CDM EXPANSION")
print("--------------------")
print(f"H0:                  {H0:.2f} km/s/Mpc")
print(f"Omega_r:             {Omega_r:.5f}")
print(f"Omega_m:             {Omega_m:.3f}")
print(f"Omega_lambda:        {Omega_lambda:.3f}")
print(f"Omega_total:         {Omega_total:.5f}")

if abs(Omega_total - 1.0) > 0.01:
    print()
    print("WARNING:")
    print("Omega_r + Omega_m + Omega_lambda is not close to 1.")
    print("This script assumes a spatially flat Universe.")


# ============================================================
# SCALE FACTOR
# ============================================================

# Logarithmic spacing is useful because cosmic history covers
# many orders of magnitude in the scale factor.

a = np.logspace(
    np.log10(a_min),
    np.log10(a_max),
    n_points
)


# ============================================================
# FRIEDMANN EQUATION
# ============================================================

# Individual terms contributing to H(a)^2 / H0^2

radiation_term = Omega_r / a**4
matter_term = Omega_m / a**3
lambda_term = Omega_lambda * np.ones_like(a)

E_squared = radiation_term + matter_term + lambda_term

# E(a) = H(a) / H0

E = np.sqrt(E_squared)

H = H0 * E


# ============================================================
# RELATIVE CONTRIBUTIONS
# ============================================================

# Fractional contribution of each component to H(a)^2.

radiation_fraction = radiation_term / E_squared
matter_fraction = matter_term / E_squared
lambda_fraction = lambda_term / E_squared


# ============================================================
# IMPORTANT TRANSITIONS
# ============================================================

# Radiation-matter equality:
#
# Omega_r / a^4 = Omega_m / a^3
#
# This transition exists only if both components are present.

if Omega_r > 0 and Omega_m > 0:
    a_rad_matter = Omega_r / Omega_m
else:
    a_rad_matter = None


# Matter-dark-energy equality:
#
# Omega_m / a^3 = Omega_lambda
#
# This transition exists only if both components are present.

if Omega_m > 0 and Omega_lambda > 0:
    a_matter_lambda = (
        Omega_m / Omega_lambda
    ) ** (1.0 / 3.0)
else:
    a_matter_lambda = None


print()
print("Characteristic transitions")
print("--------------------------")

if a_rad_matter is not None:
    print(
        f"Radiation-matter equality:   "
        f"a = {a_rad_matter:.4e}"
    )
else:
    print(
        "Radiation-matter equality:   "
        "not present in this model"
    )

if a_matter_lambda is not None:
    print(
        f"Matter-dark energy equality: "
        f"a = {a_matter_lambda:.3f}"
    )
else:
    print(
        "Matter-dark energy equality: "
        "not present in this model"
    )


# ============================================================
# PRESENT-DAY CHECK
# ============================================================

E_today = np.sqrt(
    Omega_r +
    Omega_m +
    Omega_lambda
)

H_today = H0 * E_today

print()
print(f"H(a=1):              {H_today:.2f} km/s/Mpc")
print()


# ============================================================
# PLOT
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    1,
    2,
    figsize=(13, 5.5)
)


# ------------------------------------------------------------
# Left panel: expansion rate
# ------------------------------------------------------------

ax1.loglog(
    a,
    E,
    linewidth=2,
    label="H(a) / H₀"
)

ax1.axvline(
    1.0,
    linestyle="--",
    alpha=0.7,
    label="Present Universe (a = 1)"
)

if a_rad_matter is not None:
    ax1.axvline(
        a_rad_matter,
        linestyle=":",
        alpha=0.7
    )

if a_matter_lambda is not None:
    ax1.axvline(
        a_matter_lambda,
        linestyle=":",
        alpha=0.7
    )

ax1.set_xlabel("Scale factor a")
ax1.set_ylabel("Normalized expansion rate H(a) / H₀")
ax1.set_title("Expansion history")
ax1.grid(alpha=0.3)
ax1.legend()


# ------------------------------------------------------------
# Right panel: relative contributions
# ------------------------------------------------------------

ax2.semilogx(
    a,
    radiation_fraction,
    label="Radiation"
)

ax2.semilogx(
    a,
    matter_fraction,
    label="Matter"
)

ax2.semilogx(
    a,
    lambda_fraction,
    color="black",
    label="Dark energy"
)

ax2.axvline(
    1.0,
    linestyle="--",
    alpha=0.7,
    label="Present Universe"
)

ax2.set_xlabel("Scale factor a")
ax2.set_ylabel("Fractional contribution to H(a)²")
ax2.set_ylim(-0.02, 1.05)
ax2.set_title("What dominates the expansion?")
ax2.grid(alpha=0.3)
ax2.legend()


# ------------------------------------------------------------
# Explanatory text
# ------------------------------------------------------------

ax1.text(
    0.04,
    0.05,
    "As the Universe expands, H(a) decreases strongly.\n"
    "At late times it approaches a constant value\n"
    "when dark energy dominates.",
    transform=ax1.transAxes,
    fontsize=9,
    va="bottom",
    bbox=dict(boxstyle="round", alpha=0.8)
)

# Build a descriptive message for the selected cosmological model

present_components = []

if Omega_r > 0:
    present_components.append("radiation")

if Omega_m > 0:
    present_components.append("matter")

if Omega_lambda > 0:
    present_components.append("dark energy")


if len(present_components) == 3:
    panel2_text = (
        "Radiation dominates first, then matter,\n"
        "and finally dark energy."
    )

elif present_components == ["matter", "dark energy"]:
    panel2_text = (
        "Matter dominates at small scale factor,\n"
        "followed by dark energy at late times."
    )

elif present_components == ["radiation", "matter"]:
    panel2_text = (
        "Radiation dominates first,\n"
        "followed by matter."
    )

elif present_components == ["radiation", "dark energy"]:
    panel2_text = (
        "Radiation dominates at small scale factor,\n"
        "followed by dark energy."
    )

elif present_components == ["radiation"]:
    panel2_text = "Radiation dominates at all epochs shown."

elif present_components == ["matter"]:
    panel2_text = "Matter dominates at all epochs shown."

elif present_components == ["dark energy"]:
    panel2_text = "Dark energy dominates at all epochs shown."

else:
    panel2_text = "No cosmological component is present."


ax2.text(
    0.04,
    0.05,
    panel2_text,
    transform=ax2.transAxes,
    fontsize=9,
    va="bottom",
    bbox=dict(boxstyle="round", alpha=0.8)
)


# ------------------------------------------------------------
# Final layout
# ------------------------------------------------------------

fig.suptitle(
    "Expansion of a Lambda-CDM Universe",
    fontsize=14
)

plt.tight_layout()


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
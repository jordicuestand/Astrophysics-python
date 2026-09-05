# Expansion History of a Lambda-CDM Universe

## 1. Overview

This Python experiment explores how the expansion rate of the Universe
changes throughout cosmic history in a simplified flat **Lambda-CDM
(ΛCDM) cosmological model**.

The previous experiment, `hubble_law.py`, introduced the present-day
Hubble constant \(H_0\).

But \(H_0\) is only the value of the Hubble parameter **today**.

In general, the expansion rate changes with cosmic time:

$$
H = H(t)
$$

Instead of time, this experiment uses the **scale factor** \(a\), with

$$
a = 1
$$

representing the present Universe.

Therefore:

- \(a < 1\): past Universe
- \(a = 1\): present Universe
- \(a > 1\): future Universe

The program shows how radiation, matter and dark energy affect the
expansion as the scale factor changes.

---

## 2. The physical model

For a spatially flat Universe containing radiation, matter and a cosmological constant, the script uses the simplified Friedmann equation:

$$ H^2(a) = H_0^2 \left( \frac{\Omega_r}{a^4} + \frac{\Omega_m}{a^3} + \Omega_\Lambda \right) $$

or, equivalently,

$$ \frac{H(a)}{H_0} = \sqrt{\frac{\Omega_r}{a^4} + \frac{\Omega_m}{a^3} + \Omega_\Lambda} $$

The three terms evolve very differently as the Universe expands:

$$
\rho_r \propto a^{-4}
$$

for radiation,

$$
\rho_m \propto a^{-3}
$$

for matter, while the energy density associated with a cosmological
constant remains constant.

This produces three characteristic cosmological regimes:

**radiation domination → matter domination → dark-energy domination**

---

## 3. What are the Omega parameters?

The script uses:

```python
Omega_r = 9.0e-5
Omega_m = 0.30
Omega_lambda = 0.70
```

These parameters describe the present-day density associated with each
component relative to the critical density.

`Omega_r` represents radiation.

`Omega_m` represents total matter. It includes both **ordinary
(baryonic) matter and dark matter**.

`Omega_lambda` represents dark energy in the form of a cosmological
constant.

For a spatially flat model:

$$
\Omega_r+\Omega_m+\Omega_\Lambda \approx 1.
$$

The program checks this sum and prints a warning if it differs
significantly from 1.

The default values are approximate values chosen to represent a
realistic present-day ΛCDM Universe while keeping the experiment simple.

---

## 4. Requirements

The script requires Python 3, NumPy and Matplotlib.

Install the required packages with:

```bash
pip install numpy matplotlib
```

Run the program with:

```bash
python lcdm_expansion.py
```

The generated figure is displayed and, by default, saved in the
`images` directory.

---

## 5. Understanding the figure

The program generates two panels.

### Left panel — Expansion history

The left panel represents:

$$
\frac{H(a)}{H_0}
$$

as a function of the scale factor.

Both axes are logarithmic because the evolution covers several orders
of magnitude.

At very small \(a\), the expansion rate is much larger than today.

As the Universe expands, \(H(a)\) decreases strongly.

When dark energy becomes dominant, the behaviour changes. In this
simplified ΛCDM model, at very large scale factor:

$$
\frac{H(a)}{H_0}
\longrightarrow
\sqrt{\Omega_\Lambda}.
$$

Therefore the Hubble parameter does not tend to zero in the far future
of this model.

The vertical line at

$$
a=1
$$

marks the present Universe.

### Right panel — What dominates the expansion?

The second panel shows the fractional contribution of each term to
\(H^2(a)\).

It makes the history of the Universe particularly easy to visualize:

- radiation dominates at very small scale factor;
- matter subsequently becomes dominant;
- dark energy dominates at late times.

The curves cross at physically meaningful epochs.

---

## 6. Radiation–matter equality

Radiation and matter contribute equally when

$$
\frac{\Omega_r}{a^4}
=
\frac{\Omega_m}{a^3}.
$$

Therefore:

$$
a_{\rm rm}
=
\frac{\Omega_r}{\Omega_m}.
$$

For the default parameters this occurs at approximately:

$$
a_{\rm rm}\approx3\times10^{-4}.
$$

Before this value radiation dominates.

After it, matter dominates until much later in cosmic history.

---

## 7. Matter–dark-energy equality

Matter and dark energy contribute equally when:

$$
\frac{\Omega_m}{a^3}
=
\Omega_\Lambda.
$$

Therefore:

$$
a_{m\Lambda}
=
\left(
\frac{\Omega_m}{\Omega_\Lambda}
\right)^{1/3}.
$$

With the default values:

$$
a_{m\Lambda}\approx0.75.
$$

Since the present corresponds to \(a=1\), this tells us that the
transition to dark-energy domination occurred relatively recently in
cosmic history.

---

## 8. Parameters you can modify

The main parameters are located near the beginning of the script:

```python
H0 = 70.0

Omega_r = 9.0e-5
Omega_m = 0.30
Omega_lambda = 0.70

a_min = 1.0e-4
a_max = 2.0
```

Changing the Omega parameters changes the cosmological model.

Changing `a_min` and `a_max` changes the period of cosmic history shown
in the figure.

The most interesting way to use this script is therefore not simply
to run it once, but to construct different model universes.

---

## 9. Experiments

### Experiment 1 — Reference ΛCDM Universe

Start with:

```python
Omega_r = 9.0e-5
Omega_m = 0.30
Omega_lambda = 0.70
```

Identify the three successive regimes in the right panel:

**radiation → matter → dark energy**

Notice also how dramatically the expansion rate changes between the
early and present Universe.

---

### Experiment 2 — Remove radiation

Try:

```python
Omega_r = 0.0
Omega_m = 0.30
Omega_lambda = 0.70
```

At recent epochs the result changes very little because the present
radiation density is extremely small.

At very small scale factor, however, the difference is fundamental:
the radiation-dominated era has disappeared.

This illustrates an important idea:

> A component that is almost negligible today may have dominated the
> Universe in the past.

---

### Experiment 3 — A matter-only Universe

Try:

```python
Omega_r = 0.0
Omega_m = 1.0
Omega_lambda = 0.0
```

There is no transition to dark-energy domination.

The expansion rate continues decreasing as the Universe expands.

Compare this model with the reference ΛCDM Universe, especially for
\(a>1\).

---

### Experiment 4 — A dark-energy-only Universe

Try:

```python
Omega_r = 0.0
Omega_m = 0.0
Omega_lambda = 1.0
```

The Friedmann equation becomes:

$$
H(a)=H_0.
$$

The normalized expansion rate is therefore constant.

This simple experiment isolates the effect of a cosmological constant.

---

### Experiment 5 — Change the matter/dark-energy balance

Compare:

```python
Omega_m = 0.50
Omega_lambda = 0.50
```

with:

```python
Omega_m = 0.10
Omega_lambda = 0.90
```

Before running the program, use

$$
a_{m\Lambda}
=
\left(
\frac{\Omega_m}{\Omega_\Lambda}
\right)^{1/3}
$$

to predict whether matter–dark-energy equality will move towards a
larger or smaller scale factor.

Then run the simulation and check your prediction.

---

### Experiment 6 — Look into the future

Change:

```python
a_max = 10.0
```

First use the reference ΛCDM parameters.

Then compare them with:

```python
Omega_r = 0.0
Omega_m = 1.0
Omega_lambda = 0.0
```

In the matter-only Universe,

$$
H(a)\rightarrow0
$$

as the Universe expands.

In the ΛCDM model,

$$
H(a)
\longrightarrow
H_0\sqrt{\Omega_\Lambda}.
$$

The two model universes therefore have very different long-term
expansion histories.

---

## 10. Understanding the Python code

The scale factors are generated with:

```python
a = np.logspace(
    np.log10(a_min),
    np.log10(a_max),
    n_points
)
```

`logspace` is used instead of a linear sequence because cosmic history
covers many orders of magnitude in \(a\).

The three terms in the Friedmann equation are then calculated
separately:

```python
radiation_term = Omega_r / a**4
matter_term = Omega_m / a**3
lambda_term = Omega_lambda * np.ones_like(a)
```

They are added:

```python
E_squared = radiation_term + matter_term + lambda_term
```

and:

```python
E = np.sqrt(E_squared)
```

where:

$$
E(a)=\frac{H(a)}{H_0}.
$$

Separating the three terms in the program is useful because it allows
their relative contributions to be calculated:

```python
radiation_fraction = radiation_term / E_squared
matter_fraction = matter_term / E_squared
lambda_fraction = lambda_term / E_squared
```

These quantities produce the right-hand panel.

---

## 11. Limitations of the model

This is an educational cosmological model.

It deliberately simplifies several aspects of precision cosmology.

In particular:

- the Universe is assumed to be spatially flat;
- radiation, matter and a cosmological constant are the only components;
- the dark-energy equation of state is not varied;
- neutrino physics is not treated separately;
- changes in the effective relativistic degrees of freedom are ignored;
- structure formation is not modelled;
- the script plots expansion as a function of scale factor rather than
  explicitly integrating cosmic time.

The model is intended to make the physical meaning of the Friedmann
equation visible, not to replace a numerical cosmology code.

---

## 12. Relation to the book

This experiment complements **Chapter 8: The Dynamics of the Universe**.

The chapter first introduces the observational expansion of the
Universe and Hubble's law.

The previous Python experiment explored that observational relation.

This second experiment takes the next step: the expansion rate itself
is allowed to evolve.

It provides a computational visualization of the simplified Friedmann
equation discussed in the chapter and of the succession of
radiation-, matter- and dark-energy-dominated epochs.

Together, the two experiments follow the same conceptual progression
as the chapter:

**observed expansion → Hubble constant → evolving Hubble parameter →
ΛCDM expansion history**
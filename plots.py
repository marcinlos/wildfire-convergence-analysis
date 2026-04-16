# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import itertools
import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# %%
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
OUTPUT_DIR = Path(os.getenv("DATA_DIR", "./plots"))

# %%
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# %%
def load_data(mesh_size, scheme, data_dir=DATA_DIR):
    path = DATA_DIR / f"nonlinear-{mesh_size}-{scheme}"
    data = np.genfromtxt(path, delimiter=";", names=True)
    ok = data["L2_rel"] < 30
    return data[ok]


# %%
def plot_data(ax, data, label, marker="o", column="L2_rel"):
    dts = 1 / data["steps"]
    vals = data[column]
    ax.loglog(dts, vals, marker=marker, label=label)


# %%
def plot_ref_line(ax, data, scale=2, column="L2_rel"):
    dts = 1 / data["steps"]
    vals = data[column]

    X = np.log(dts)
    Y = np.log(vals)

    c = np.polyfit(X, Y - X, deg=0)
    ref = scale * np.exp(c) * dts

    p2 = (dts[0], ref[0])
    p1 = (dts[-1], ref[-1])

    p1_disp = ax.transData.transform(p1)
    p2_disp = ax.transData.transform(p2)

    dx = p2_disp[0] - p1_disp[0]
    dy = p2_disp[1] - p1_disp[1]

    # We subtract 2.5 degrees, because there is some weird
    # upwards drift otherwise
    angle = np.degrees(np.arctan2(dy, dx))

    s = 0.5
    px = p1[0] ** (1 - s) * p2[0] ** s
    py = p1[1] ** (1 - s) * p2[1] ** s

    # 3. Add rotated text
    ax.text(
        px,
        py,
        r"order = 1",
        rotation=angle,
        rotation_mode="anchor",
        va="bottom",
    )

    ax.loglog(dts, ref, linestyle="--", color="black", linewidth=0.5)


# %%
configs = list(itertools.product([50, 100, 200], ["PR", "strang-CN", "FE"]))
data = {f"{n}-{scheme}": load_data(n, scheme) for n, scheme in configs}

# %%
# data["200-FE"] = data["200-FE"][1:]

# %%
for n in (50, 100, 200):
    fig, ax = plt.subplots()

    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel("relative error at $T = 1$")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    plot_data(ax, data[f"{n}-PR"], marker="o", label="Peaceman-Rachford")
    plot_data(ax, data[f"{n}-strang-CN"], marker="s", label="Strang + CN")
    plot_data(ax, data[f"{n}-FE"], marker="D", label="Explicit")

    ref_data = data[f"{n}-PR"]
    plot_ref_line(ax, ref_data)

    ax.legend()
    fig.savefig(OUTPUT_DIR / f"convergence-{n}x{n}.pdf", bbox_inches="tight")

# %%

# %%

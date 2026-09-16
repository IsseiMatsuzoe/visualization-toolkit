from __future__ import annotations

from typing import Sequence
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def _finish(fig, output_path=None):
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path, bbox_inches="tight")
    return fig


def render_bloch_sphere(
    theta: float,
    phi: float,
    title: str | None = None,
    output_path: str | None = None,
):
    """Render a simple 3D Bloch sphere with one state vector."""
    fig = plt.figure(figsize=(5.5, 5.5))
    ax = fig.add_subplot(111, projection="3d")

    u = np.linspace(0, 2 * np.pi, 72)
    v = np.linspace(0, np.pi, 36)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x, y, z, rstride=6, cstride=6, linewidth=0.45)

    sx = np.sin(theta) * np.cos(phi)
    sy = np.sin(theta) * np.sin(phi)
    sz = np.cos(theta)
    ax.quiver(0, 0, 0, sx, sy, sz, arrow_length_ratio=0.12, linewidth=2)

    ax.text(0, 0, 1.12, "|0>", ha="center")
    ax.text(0, 0, -1.18, "|1>", ha="center")
    ax.text(sx, sy, sz, "  |ψ>", fontsize=10)

    lim = 1.15
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    if title:
        ax.set_title(title)
    return _finish(fig, output_path)


def render_state_graph(
    nodes: Sequence[str],
    edges: Sequence[tuple[str, str]],
    title: str | None = None,
    output_path: str | None = None,
):
    """Render a small directed state/dependency graph without graphviz."""
    n = len(nodes)
    if n == 0:
        raise ValueError("nodes cannot be empty")

    angles = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, n, endpoint=False)
    pos = {node: (np.cos(a), np.sin(a)) for node, a in zip(nodes, angles)}

    fig, ax = plt.subplots(figsize=(6, 5.5))
    for node, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.14, fill=False, linewidth=1.8))
        ax.text(x, y, node, ha="center", va="center", fontsize=9)

    for a, b in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        dx, dy = x2 - x1, y2 - y1
        ax.annotate(
            "",
            xy=(x2 - 0.16 * dx, y2 - 0.16 * dy),
            xytext=(x1 + 0.16 * dx, y1 + 0.16 * dy),
            arrowprops={"arrowstyle": "->", "linewidth": 1.2},
        )

    ax.set_aspect("equal")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    if title:
        ax.set_title(title)
    return _finish(fig, output_path)


def render_function_plot(
    x,
    y,
    xlabel: str = "x",
    ylabel: str = "y",
    title: str | None = None,
    output_path: str | None = None,
):
    """Render a clean 2D function/data plot."""
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(x, y)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.25)
    return _finish(fig, output_path)

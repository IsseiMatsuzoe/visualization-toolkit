from __future__ import annotations

import math
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

NOTE_TO_PC = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "Fb": 4, "E#": 5, "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10,
    "B": 11, "Cb": 11, "B#": 0,
}
PC_TO_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
STANDARD_TUNING = ["E", "A", "D", "G", "B", "E"]  # low -> high


def _finish(fig, output_path=None):
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path, bbox_inches="tight")
    return fig


def render_keyboard(
    notes: Sequence[str],
    labels: Sequence[str] | None = None,
    octaves: int = 1,
    title: str | None = None,
    output_path: str | None = None,
):
    """Render a compact piano keyboard. Notes are pitch classes, e.g. C, Eb, G."""
    if labels is None:
        labels = list(notes)
    if len(labels) != len(notes):
        raise ValueError("labels must have the same length as notes")

    highlight = {NOTE_TO_PC[n]: labels[i] for i, n in enumerate(notes)}
    white_pcs = [0, 2, 4, 5, 7, 9, 11]
    black_after = {0: 1, 2: 3, 5: 6, 7: 8, 9: 10}

    fig, ax = plt.subplots(figsize=(max(6, 7 * octaves * 0.8), 2.7))

    x = 0
    for _ in range(octaves):
        for pc in white_pcs:
            ax.add_patch(Rectangle((x, 0), 1, 4, fill=False, linewidth=1.2))
            if pc in highlight:
                is_root = str(highlight[pc]).strip() in {"1", "R", "root", "Root"}
                ax.add_patch(
                    Circle(
                        (x + 0.5, 0.75),
                        0.20 if is_root else 0.17,
                        fill=is_root,
                        linewidth=1.5,
                    )
                )
                ax.text(x + 0.5, 0.75, highlight[pc], ha="center", va="center", fontsize=9)
            x += 1

    x = 0
    for _ in range(octaves):
        for pc in white_pcs:
            if pc in black_after:
                black_pc = black_after[pc]
                ax.add_patch(Rectangle((x + 0.68, 1.75), 0.64, 2.25, fill=False, linewidth=2.0))
                if black_pc in highlight:
                    is_root = str(highlight[black_pc]).strip() in {"1", "R", "root", "Root"}
                    ax.add_patch(
                        Circle(
                            (x + 1.0, 2.25),
                            0.17 if is_root else 0.14,
                            fill=is_root,
                            linewidth=1.5,
                        )
                    )
                    ax.text(x + 1.0, 2.25, highlight[black_pc], ha="center", va="center", fontsize=8)
            x += 1

    ax.set_xlim(0, 7 * octaves)
    ax.set_ylim(0, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title)
    return _finish(fig, output_path)


def render_fretboard(
    root: str,
    notes: Sequence[str],
    labels: Sequence[str] | None = None,
    frets: int = 12,
    tuning: Sequence[str] = STANDARD_TUNING,
    title: str | None = None,
    output_path: str | None = None,
):
    """Render guitar fretboard with deterministic pitch-class locations."""
    if labels is None:
        labels = list(notes)
    if len(labels) != len(notes):
        raise ValueError("labels must have the same length as notes")

    label_by_pc = {NOTE_TO_PC[n]: labels[i] for i, n in enumerate(notes)}
    root_pc = NOTE_TO_PC[root]

    fig, ax = plt.subplots(figsize=(max(8, frets * 0.72), 3.8))

    ax.vlines(range(frets + 1), 0, len(tuning) - 1, linewidth=1)
    for fret_number in range(1, frets + 1):
        ax.text(fret_number - 0.5, -0.55, str(fret_number), ha="center", va="center", fontsize=8)

    ax.hlines(range(len(tuning)), 0, frets, linewidth=1)
    for string_index, open_note in enumerate(tuning):
        open_pc = NOTE_TO_PC[open_note]
        ax.text(-0.72, string_index, open_note, ha="right", va="center", fontsize=9)
        for fret in range(frets + 1):
            pc = (open_pc + fret) % 12
            if pc in label_by_pc:
                x = -0.35 if fret == 0 else fret - 0.5
                is_root = pc == root_pc
                size = 0.23 if is_root else 0.18
                ax.add_patch(Circle((x, string_index), size, fill=is_root, linewidth=1.5))
                ax.text(x, string_index, label_by_pc[pc], ha="center", va="center", fontsize=7)

    ax.text(-0.35, -0.55, "open", ha="center", va="center", fontsize=8)
    ax.set_xlim(-1.05, frets + 0.1)
    ax.set_ylim(-0.9, len(tuning) - 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title)
    return _finish(fig, output_path)


def render_interval_map(
    root: str,
    targets: Sequence[str],
    labels: Sequence[str] | None = None,
    title: str | None = None,
    output_path: str | None = None,
):
    """Render semitone distances around a 12-step pitch-class ring."""
    if labels is None:
        labels = list(targets)
    if len(labels) != len(targets):
        raise ValueError("labels must have the same length as targets")

    root_pc = NOTE_TO_PC[root]
    pcs = [NOTE_TO_PC[n] for n in targets]

    display_name = {pc: PC_TO_SHARP[pc] for pc in range(12)}
    display_name[root_pc] = root
    for note in targets:
        display_name[NOTE_TO_PC[note]] = note

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    for pc in range(12):
        theta = math.pi / 2 - 2 * math.pi * pc / 12
        x, y = math.cos(theta), math.sin(theta)
        ax.add_patch(Circle((x, y), 0.08, fill=False))
        ax.text(x, y, display_name[pc], ha="center", va="center", fontsize=8)

    root_theta = math.pi / 2 - 2 * math.pi * root_pc / 12
    root_x, root_y = math.cos(root_theta), math.sin(root_theta)
    ax.add_patch(Circle((root_x, root_y), 0.13, fill=False, linewidth=2.2))

    for pc, label in zip(pcs, labels):
        theta = math.pi / 2 - 2 * math.pi * pc / 12
        x, y = math.cos(theta), math.sin(theta)

        # Keep the original long radial arrow and label placement.
        # Pitch markers have radius 0.08 on a unit ring, so radius 0.92 is
        # exactly their inner edge along the radial direction. This prevents
        # arrowheads from intruding into the note marker while preserving the
        # original label/arrow geometry.
        ax.annotate(
            f"{label}\n+{(pc - root_pc) % 12}",
            xy=(0.92 * x, 0.92 * y),
            xytext=(0.58 * x, 0.58 * y),
            ha="center",
            va="center",
            arrowprops={"arrowstyle": "->", "linewidth": 1},
            fontsize=9,
        )

    ax.set_aspect("equal")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.axis("off")
    if title:
        ax.set_title(title)
    return _finish(fig, output_path)

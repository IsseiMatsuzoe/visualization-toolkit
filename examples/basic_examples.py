from visual_teaching_toolkit import render
import numpy as np

render({
    "type": "fretboard",
    "root": "D",
    "notes": ["D", "E", "F", "G", "A", "B", "C"],
    "labels": ["1", "2", "b3", "4", "5", "6", "b7"],
    "frets": 12,
    "title": "D Dorian on guitar",
}, "d_dorian.svg")

render({
    "type": "keyboard",
    "notes": ["C", "Eb", "G"],
    "labels": ["1", "b3", "5"],
    "title": "C minor triad",
}, "c_minor_keyboard.svg")

render({
    "type": "bloch_sphere",
    "theta": float(np.pi / 3),
    "phi": float(np.pi / 4),
    "title": "Bloch sphere",
}, "bloch.svg")

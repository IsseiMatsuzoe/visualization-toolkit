from __future__ import annotations
from typing import Any, Dict

from .music import render_keyboard, render_fretboard, render_interval_map
from .science import render_bloch_sphere, render_state_graph, render_function_plot

_RENDERERS = {
    "keyboard": render_keyboard,
    "fretboard": render_fretboard,
    "interval_map": render_interval_map,
    "bloch_sphere": render_bloch_sphere,
    "state_graph": render_state_graph,
    "function_plot": render_function_plot,
}


def render(spec: Dict[str, Any], output_path: str | None = None):
    """Render one visual from a compact structured spec."""
    kind = spec.get("type")
    if kind not in _RENDERERS:
        raise ValueError(f"Unknown visual type: {kind!r}. Available: {sorted(_RENDERERS)}")
    kwargs = {k: v for k, v in spec.items() if k != "type"}
    if output_path is not None:
        kwargs["output_path"] = output_path
    return _RENDERERS[kind](**kwargs)

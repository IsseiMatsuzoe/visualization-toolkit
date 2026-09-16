# Visual Teaching Toolkit

A small deterministic rendering layer for visual-first explanations.

The design goal is simple:

**LLM chooses meaning -> renderer computes geometry -> chat shows a stable visual.**

It intentionally avoids generative-image models for diagrams where position, labeling, and topology matter.

Current package version: **0.3.0**.

## Current renderers

### Music
- `keyboard(...)`
- `fretboard(...)`
- `interval_map(...)`

### Math / Physics
- `bloch_sphere(...)`
- `state_graph(...)`
- `function_plot(...)`

## Structured interface

The preferred interface for ChatGPT / future Apps SDK integration is one compact dictionary:

```python
from visual_teaching_toolkit import render

render({
    "type": "fretboard",
    "root": "D",
    "notes": ["D", "E", "F", "G", "A", "B", "C"],
    "labels": ["1", "2", "b3", "4", "5", "6", "b7"],
    "frets": 12,
}, "d_dorian.svg")
```

This separation is intentional. A future ChatGPT App can send the same spec to a browser-side renderer without changing the reasoning layer.

## Development

Install in editable mode:

```bash
python -m pip install -e .
```

Run the geometry tests:

```bash
python -m pytest -q tests
```

Generate the basic examples:

```bash
python examples/basic_examples.py
```

## Design principles

1. Geometry must be deterministic.
2. Labels stay near the object they explain without obscuring it.
3. Prefer motion, change, and comparison over long verbal definitions.
4. Each figure should answer one visual question.
5. Visuals are explanatory aids, not decoration.
6. Formal terminology comes after the spatial or structural model when teaching a new concept.
7. Preserve stable visual grammar across revisions; fix local collisions without unnecessarily changing the overall geometry.

For interval maps specifically, radial arrows should retain their readable length and label origin while terminating at the boundary of the pitch-class marker rather than intruding into it.

## Future App architecture

```text
ChatGPT reasoning
      |
      | compact JSON-like spec
      v
Visual Teaching Toolkit
      |
      +-- SVG / Canvas renderer
      |
      v
interactive in-chat widget
```

For a future Apps SDK version, keep these renderer primitives stable and replace only the presentation layer.

See `docs/APP_MIGRATION.md` for the intended migration path.

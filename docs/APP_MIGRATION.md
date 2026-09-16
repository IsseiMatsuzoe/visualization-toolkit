# Future ChatGPT App migration

The toolkit deliberately keeps reasoning and rendering separate.

Current:
1. ChatGPT chooses a compact render spec.
2. Python renderer converts the spec into SVG/PNG.
3. The visual is shown in the chat.

Future ChatGPT App:
1. ChatGPT chooses the same render spec.
2. An App tool receives the spec.
3. Browser-side SVG/Canvas components render it interactively.
4. Optional interactions update local UI state.

The renderer contract should remain stable. The first App version should expose only a small tool surface such as:

- `render_visual(spec)`
- optionally `play_notes(notes)` for music

Do not expose one tool per visual primitive unless there is a concrete need.

Recommended interactive upgrades:
- keyboard: tap a key to hear it; toggle degree/note labels
- fretboard: highlight root, scale degrees, chord tones, or one position
- interval map: click a degree to hear the interval
- Bloch sphere: drag theta/phi and update the state vector
- state graph: highlight one path at a time

Keep correctness-critical geometry deterministic. Do not replace these diagrams with image generation.

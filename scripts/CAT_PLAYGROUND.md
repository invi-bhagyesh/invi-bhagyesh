# Cat playground

The original ginger pixel cat plays fetch with a blue-grey companion. Ginger
uses a portal shortcut while slate wakes up, returns the ball, and naps.
The standalone SVG sits near the top of the README; it needs no network calls.

## Regenerate

```sh
python3 scripts/cat_playground.py
```

The 24-second loop shares explicit paw-contact times (4, 6, and 10 seconds).
Ball flight uses gravity and restitution 0.45; rolling slows with friction.
Portal entry/exit use spatial clipping instead of opacity fades. Every pose is
anchored to the same floor, with normalized head sizes and three in-between
frames for standing and curling up. Reduced motion shows a static scene.

Normalized sprites are committed. To rebuild them from the original artwork,
install Pillow and run `python3 scripts/prepare_cat_sprites.py`, then regenerate
the SVG. Palette conversion preserves outlines and eye details.

# Cat playground

A self-contained SVG using the original orange pixel-cat sprites from the website.
Two cats chase and bat a bouncing ball; one leaps through portals. The 20-second
loop includes idle pauses and a static reduced-motion fallback. It uses no
contribution data, external image requests, or scheduled refresh workflow.

Regenerate after edits:

```sh
python3 scripts/cat_playground.py
```

The generator embeds `assets/cat-walk-left.png` and `assets/cat-awake.png` in
`assets/cat-playground.svg`. Commit the regenerated SVG along with source edits.

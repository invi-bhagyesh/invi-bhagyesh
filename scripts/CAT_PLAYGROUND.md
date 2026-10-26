# Cat playground

The original ginger pixel cat plays fetch with a cocoa-and-cream companion. Ginger
uses a portal shortcut while cocoa wakes up, returns the ball, and naps.
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

Cats and ball render at 1.5× the original size. Contact positions and portal
clearance account for the larger silhouettes. Original platformer scenery adds
grassy brick ground, distant hills, clouds, and paw-print blocks, with light
and dark palettes. The generated sprite assets use the ginger and cocoa names.

## Character and story timing

Ginger has an eager, upright-tail trot. Cocoa uses shorter steps, a lowered
curved tail, and a tucked-paw loaf. Gait frames advance from actual distance
travelled while grounded; stationary poses and jumps do not advance the feet.
The teleport displacement is excluded from travelled distance.

Dialogue follows the shared scene clock: an invitation, agreement, the throw,
Cocoa noticing the portal shortcut, Ginger's reply, and Cocoa choosing a nap.
Ginger asks for a rematch after waking. Only one speech bubble appears at a time;
reduced motion hides dialogue and shows a still scene. The SVG description also
provides the conversation for readers who cannot see the animation.

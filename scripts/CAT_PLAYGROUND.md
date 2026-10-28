# Cat playground

The original ginger pixel cat plays fetch with a white companion. Nivi
uses a portal shortcut while Livi wakes up, returns the ball, and naps.
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
and dark palettes. The generated sprite assets use the nivi and livi names.

## Character and story timing

Nivi has an eager trot. Livi, the white cat, takes a slower-paced walk. Both
use complete source frames; the earlier cropped-leg and tail edits were removed
because they broke the silhouette. White fur retains darker outlines for contrast. Gait frames advance from actual distance
travelled while grounded; stationary poses and jumps do not advance the feet.
The teleport displacement is excluded from travelled distance.

Dialogue follows the shared scene clock: an invitation, agreement, the throw,
Livi noticing the portal shortcut, Nivi's reply, and Livi choosing a nap.
Nivi asks for a rematch after waking. Only one speech bubble appears at a time;
reduced motion hides dialogue and shows a still scene. The SVG description also
provides the conversation for readers who cannot see the animation.

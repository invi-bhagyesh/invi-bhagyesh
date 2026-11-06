# Cat playground

The original ginger pixel cat plays fetch with an apricot-orange spotted companion. Nivi
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

Nivi has an eager trot. Livi, the apricot-orange spotted cat, takes a slower-paced walk. Both
use complete source frames; the earlier cropped-leg and tail edits were removed
because they broke the silhouette. Apricot fur retains darker outlines and russet spots for contrast. Gait frames advance from actual distance
travelled while grounded; stationary poses and jumps do not advance the feet.
The teleport displacement is excluded from travelled distance.

Dialogue follows the shared scene clock: an invitation, agreement, the throw,
Livi noticing the portal shortcut, Nivi's reply, and Livi choosing a nap.
Nivi asks for a rematch after waking. Only one speech bubble appears at a time;
reduced motion hides dialogue and shows a still scene. The SVG description also
provides the conversation for readers who cannot see the animation.

Walking uses 32 generated frames with a shared torso and articulated legs, avoiding
frame-to-frame silhouette shifts. Nivi trots with diagonal pairs; Livi walks with
staggered footfalls and a longer planted phase. The stride covers 24 or 20 sprite
pixels respectively, multiplied by the display scale. Each planted paw moves
backwards relative to the body at the same rate the body moves forwards; swing
phases lift and return the paw. Pixel rounding leaves less than 3 screen pixels of
contact drift. Positions are sampled at 60 Hz and retain subpixel precision.
Airborne and ball-tap poses hold still rather than cycling the legs. A keyframe
immediately before teleport prevents a visible slide between the two portals.
